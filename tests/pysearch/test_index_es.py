import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import numpy as np
import pandas as pd 

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

ELASTIC_PORT = os.environ.get("ELASTIC_PORT", None)
ELASTIC_USERNAME = os.environ.get("ELASTIC_USERNAME", None)
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD", None)

assert ELASTIC_PORT is not None, "ELASTIC_PORT is not set"
assert ELASTIC_USERNAME is not None, "ELASTIC_USERNAME is not set"
assert ELASTIC_PASSWORD is not None, "ELASTIC_PASSWORD is not set"

from pysearch.elastic import ElasticProcessor

config = {
    # Global config
    "HOST": "0.0.0.0",
    "PORT": ELASTIC_PORT,
    "USERNAME": ELASTIC_USERNAME,
    "PASSWORD": ELASTIC_PASSWORD,
    "INDEX": "test_index",
    "RETURN_SIZE": 10,
    "CACHE_DIR": ".cache/",
    "DIMENSION": 768,
}

def test_index_document():
    
    def gendata(n: int = 10):
        features = np.ones((n, 768), dtype=float)
        features = features * np.arange(n).reshape(-1, 1)

        # df from dict 
        df = pd.DataFrame.from_dict({
            'index':  [f'image{x}' for x in range(n)], \
            'field1': [f'string{x}' for x in range(n)], \
            'field2': [x for x in range(n)], \
            'field3': [x for x in range(n)], \
            'feature': features.tolist() \
        })
        return df
    proc = ElasticProcessor(config)
    df = gendata()
    df_structure = {  
        "mappings": {
            "properties": {
                "index": {"type": "integer"},
                "field1": {"type": "text"},
                "field2": {"type": "integer"},
                "field3": {"type": "integer"},
                "feature": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "l2_norm"}
            }
        }
    }

    proc.index_dataframe(df, df_structure)

def test_search():
    proc = ElasticProcessor(config)
    print(proc.info())
    results = proc.search(text_query='string1', fields=['field1'])
    from pprint import pprint
    pprint(results)

def test_get_by_id():
    proc = ElasticProcessor(config)
    tmp = proc.get_document_by_id("image1")
    from pprint import pprint
    pprint(tmp)

def test_search_filter():
    proc = ElasticProcessor(config)
    print(proc.info())
    results = proc.search(text_query='string1', fields=['field1'], filter=['image2'])
    from pprint import pprint
    pprint(results)

test_index_document()
# test_search()
# test_get_by_id()
test_search_filter()