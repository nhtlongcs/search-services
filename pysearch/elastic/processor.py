import json
from pysearch.utils import time_this
from elasticsearch import Elasticsearch, RequestsHttpConnection
from .query_generator import QueryGenerator
from elasticsearch.helpers import bulk
import argparse
from pysearch.base.processor import Processor
from tqdm import tqdm 
from typing import List, Dict, Any, Union, Optional

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
    def search(self, text_query, fields, filter=None, time_range=None):
        """
            text_query: string
            filter: list of document ids

            This function will return a list of documents that match the query
            Text query is analysed by the analyser
            Use filter to limit the search to a set of documents, if filter is None, document_set is ignored
        """
        self.generator = QueryGenerator(self.client, self.index)
        # self.generator.reset_query()
        self._filter(filter)
        self._search_normal_fields(fields, text_query, text_query)
        # self._search_time_fields(fields, time_range)
        query = self.generator.run(profiler=False)
        print(query)
        result = self.client.search(index=self.index, body=json.dumps(query), size=self.return_size)
        return result['hits']['hits']
    
    def _filter(self, filter: Optional[List[str]] = None):
        if filter is not None and len(filter) > 0 :
            self.generator.add_document_set(filter)

    def _search_normal_fields(self, fields, must_part, should_part):
        assert isinstance(fields, list), "fields must be a list"
        assert isinstance(must_part, str), "must_part must be a string, only one string is allowed"
        assert isinstance(should_part, str), "should_part must be a string, only one string is allowed"

        # todo: check if fields are valid

        self.generator.gen_query_string_query(fields, must_part, False)
        self.generator.gen_query_string_query(fields, should_part, True)
    
    def _search_time_fields(self, fields, time_range):
        # value_from, value_to = time_range
        # self.generator.gen_range_query(value_type, value_from, value_to, value_format)
        # self.generator.gen_time_query(fields, must_parts, False)
        # self.generator.gen_time_query(fields, should_parts, True)
        assert NotImplementedError, "Time query is not available yet"
    
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

