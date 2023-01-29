import os
from dotenv import load_dotenv
from pathlib import Path
from elasticsearch import Elasticsearch, RequestsHttpConnection

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

ELASTIC_PORT = os.environ.get("ELASTIC_PORT", None)

assert ELASTIC_PORT is not None, "ELASTIC_PORT is not set"

def test_es_connection():
    es = Elasticsearch([f'http://0.0.0.0:{ELASTIC_PORT}'], timeout=100, connection_class=RequestsHttpConnection, http_auth=('elastic', '123456'), use_ssl=False, verify_certs=False)