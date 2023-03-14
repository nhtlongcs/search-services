import json
from pysearch.utils import time_this
from elasticsearch import Elasticsearch, RequestsHttpConnection
from .query_generator import QueryGenerator
from elasticsearch.helpers import bulk
import argparse
from pysearch.base.processor import Processor
from tqdm import tqdm 
from typing import List, Dict, Any, Union, Optional
from datetime import datetime

class ElasticProcessor(Processor):
    def __init__(self, config):
        # convert dict to namespace
        config = argparse.Namespace(**config)

        self.host = config.HOST
        self.port = config.PORT
        self.index = config.INDEX
        self.username = config.USERNAME
        self.password = config.PASSWORD
        self.return_size = config.RETURN_SIZE
        self.client = self._connect()
        # self.analyser = QueryAnalyser(self.generator)
    
    def index_dataframe(self, df, df_structure):

        self.client.indices.delete(index=self.index, ignore=[400, 404])
        self.client.indices.create(index=self.index, body=df_structure, ignore=400)
        self.client.indices.get_alias("*")

        def index_iterator(df):
            for i, row in tqdm(df.iterrows(), total=len(df)):
                data = row.to_dict()
                index = data.pop('index', None)
                yield {
                    "_index": self.index,
                    "_id": index,
                    "_source": data
                }
        bulk(self.client, index_iterator(df))
        self.client.indices.refresh(index=self.index)
        
    def _connect(self):
        es = Elasticsearch([f'http://0.0.0.0:{self.port}'],
                        timeout=100, \
                        connection_class=RequestsHttpConnection, 
                        http_auth=(self.username, self.password), 
                        use_ssl=False, 
                        verify_certs=False)
        if es.ping():
            print("Connected to Elasticsearch node")
        else:
            print("Error: Cannot connect to Elasticsearch cluster")
        return es
    
    """
    Main function for searching in elasticsearch
    """
    @time_this
    def search(self, **kwargs):
        """
        Default search function is to search by text in time range
        """
        return self.search_text_inrange_pipeline(**kwargs)
    

    def search_filter_only(self, filter: List[str]):
        """
            Example: search_filter_only(['image1', 'image2'])
        """
        return self.compose_pipeline({ 'filter': filter})

    def search_text_closestday_pipeline(self, text_query: str, fields: List[str], filter: List[str], timefield: str, timestamp: datetime):
        """
            Example: search_text_inrange_pipeline('text', ['field1', 'field2'], \
                ['image1', 'image2'], 'timestamp', '20200101', '20200110')
            The steps are:
            1. Filter by document set
            2. Search by scoring (text in fields and time)
            3. Return the result
        """
        return  self.compose_pipeline({'filter': filter, 'text': {'fields': fields, 'should': text_query, 'must': None}, \
                                       'time': {'field': timefield, 'timestamp': timestamp}})
    
    def search_text_inrange_pipeline(self, text_query: str, fields: List[str], filter: List[str], \
                                     timefield: str, start: datetime, end: datetime):

        """
            Example: search_text_inrange_pipeline('text', ['field1', 'field2'], \
                ['image1', 'image2'], 'timestamp', '20200101', '20200110')
            The steps are:
            1. Filter by document set
            2. Filter by time range
            3. Search text in fields
            4. Return the result
        """
        return self.compose_pipeline({  'filter': filter, 'time': {'field': timefield, 'start': start, 'end': end}, \
                                        'text': {'fields': fields, 'should': text_query, 'must': None}})

    def search_timestamp_pipeline(self, timefield: str, timestamp: datetime, filter: List[str]):
        """
            Example: search_time_range_pipeline('timestamp', '20200101', '20200110', ['image1', 'image2'])
            The steps are:
            1. Filter by document set
            2. Find top nearest timestamp
            3. Return the result
        """
        return self.compose_pipeline({'filter': filter, 'time': {'field': timefield, 'timestamp': timestamp}})
    
    def search_time_range_pipeline(self, timefield: str, start: datetime, end: datetime, filter: List[str]):
        """
            Example: search_time_range_pipeline('timestamp', '20200101', '20200110', ['image1', 'image2'])
            The steps are:
            1. Filter by document set
            2. Filter by time range
            3. Return the result
        """
        return self.compose_pipeline({'filter': filter, 'time': {'field': timefield, 'start': start, 'end': end}})

    def compose_pipeline(self, query: dict, topk: Optional[int] = None):
        """
            Example: compose_pipeline({'filter': ['image1', 'image2'], \
                'time': {'field': 'timestamp', 'start': '20200101', 'end': '20200110'}, \
                'text': {'fields': ['field1', 'field2'], 'must': 'text1', 'should': 'text2'}})
            The steps are:
            1. Filter by document set
            2. Filter by time range
            3. Search text in fields
            4. Return the result
        """
        topk = self.return_size if topk is None else topk
        self.generator = QueryGenerator(self.client, self.index)
        assert len(query) > 0, "Query cannot be empty"
        if query.get('filter') is not None:
            self._filter(query['filter'])
        if query.get('time') is not None:
            if 'timestamp' in query['time'].keys():
                self._search_time_fields(query['time']['field'], query['time']['timestamp'])
            else:
                self._search_time_fields(query['time']['field'], (query['time']['start'], query['time']['end']))
    
        if query.get('text') is not None:
            self._search_normal_fields(query['text']['fields'], query['text']['must'], query['text']['should'])

        query = self.generator.run(profiler=False)
        import pdb; pdb.set_trace()
        result = self.client.search(index=self.index, body=json.dumps(query), size=topk)
        return result['hits']['hits']

    def _filter(self, filter: Optional[List[str]] = None):
        if filter is not None and len(filter) > 0 :
            self.generator.add_document_set(filter)

    def _search_normal_fields(self, fields, must_part, should_part):
        # https://stackoverflow.com/questions/28768277/elasticsearch-difference-between-must-and-should-bool-query

        assert isinstance(fields, list), "fields must be a list"

        # todo: check if fields are valid
        if must_part is not None:
            assert isinstance(must_part, str), "must_part must be a string, only one string is allowed"
            self.generator.gen_query_string_query(fields, must_part, False)
        if should_part is not None:
            assert isinstance(should_part, str), "should_part must be a string, only one string is allowed"
            self.generator.gen_query_string_query(fields, should_part, True)
    
    def _search_time_fields(self, timefield, timestamp):
        def _search_closest_time(timefield, timestamp):
            assert isinstance(timestamp, datetime), "timestamp must be a datetime object"
            timestamp = timestamp.strftime("%Y%m%d")
            self.generator.gen_closest_time_query(timefield, timestamp)

        def _search_time_range(timefield, timestamp):
            from_, to_ = timestamp
            from_ = from_.strftime("%Y%m%d")
            to_ = to_.strftime("%Y%m%d")
            # https://www.elastic.co/guide/en/elasticsearch/reference/2.0/mapping-date-format.html#built-in-date-formats
            self.generator.gen_range_query(timefield, from_, to_, 'basic_date')
        
        if timestamp is None or (isinstance(timestamp, tuple) and (timestamp[0] is None or timestamp[1] is None)):
            # do nothing
            return
        
        if isinstance(timestamp, datetime):    
            _search_closest_time(timefield, timestamp)
        elif isinstance(timestamp, tuple) and list(map(type, timestamp)) == [datetime, datetime]:
            _search_time_range(timefield, timestamp)
        else:
            raise ValueError("timestamp must be a datetime object or a tuple of datetime objects")
    
    def info(self):
        super().info()

    @time_this
    def get_document_by_id(self, ids):
        query = {
            "query": {
                "ids" : {
                    "values" : ids
                }
            }
        }
        result = self.client.search(query, size=self.return_size)
        return result['hits']['hits']

