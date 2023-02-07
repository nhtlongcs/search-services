import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import numpy as np

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

CLIP_PORT = os.environ.get("CLIP_PORT", None)
MILVUS_PORT = os.environ.get("MILVUS_PORT", None)

assert CLIP_PORT is not None, "CLIP_PORT is not set"
assert MILVUS_PORT is not None, "MILVUS_PORT is not set"

from pysearch.milvus import Milvus2Processor as MilvusProcessor
config = {
    # Global config
    "HOST": "localhost",
    "PORT": MILVUS_PORT,
    "INDEX": "test_index",
    "RETURN_SIZE": 10,
    "CACHE_DIR": ".cache/",
    # Milvus config
    "DIMENSION": 768,
}
def test_index_document():
    """
    Test indexing a list of documents

    features: np.ndarray
        [0. 0. 0. 0. 0. 0. 0. 0. 0. 0...]
        [1. 1. 1. 1. 1. 1. 1. 1. 1. 1...]
        [2. 2. 2. 2. 2. 2. 2. 2. 2. 2...]
        [3. 3. 3. 3. 3. 3. 3. 3. 3. 3...]
        [4. 4. 4. 4. 4. 4. 4. 4. 4. 4...]
        [5. 5. 5. 5. 5. 5. 5. 5. 5. 5...]
        [6. 6. 6. 6. 6. 6. 6. 6. 6. 6...]
        [7. 7. 7. 7. 7. 7. 7. 7. 7. 7...]
        [8. 8. 8. 8. 8. 8. 8. 8. 8. 8...]
        [9. 9. 9. 9. 9. 9. 9. 9. 9. 9...]
    image_names: List[str]
        ["image10", "image9",.. "image2", "image1"]
    """
    proc = MilvusProcessor(config)
    features = np.ones((10, 768))
    features = features * np.arange(10).reshape(-1, 1)
    
    image_names = [f"image{i}" for i in range(10)]
    proc.index_list_document(features, image_names)

def test_search():
    query = np.ones((1, 768)) * 7
    proc = MilvusProcessor(config)
    print(proc.info())
    results = proc.search(query, top_k=10)
    from pprint import pprint
    pprint(results)


def test_search_filter():
    query = np.ones((1, 768)) * 7
    proc = MilvusProcessor(config)
    print(proc.info())
    results = proc.search(query, top_k=10, filter=["image7", "image8", "image9"])
    from pprint import pprint
    pprint(results)

test_index_document()
test_search()
test_search_filter()