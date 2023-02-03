# write a code to index vector data into elasticsearch
import pandas as pd 
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch, RequestsHttpConnection
import numpy as np
from tqdm import tqdm
es = Elasticsearch(['http://0.0.0.0:20542'], timeout=100, connection_class=RequestsHttpConnection, http_auth=('elastic', '123456'), use_ssl=False, verify_certs=False)

es.indices.create(index='test', ignore=400)
es.indices.get_alias("*")

n = 3 

features = np.ones((n, 768))
features = features * np.arange(n).reshape(-1, 1)

# df from dict 
df = pd.DataFrame.from_dict({
    'index':  [1, 2, 3], \
    'field1': [1, 2, 3], \
    'field2': [1, 2, 3], \
    'field3': [1, 2, 3], \
    'feature': features.tolist() \
})

def gen_data():
    for i, row in tqdm(df.iterrows(), total=len(df)):
        data = row.to_dict()
        data.pop('index', None)
        yield {
            "_index": 'test',
            "_id": row['index'],
            "_source": data
        }