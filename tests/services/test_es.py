import os
from dotenv import load_dotenv
from pathlib import Path
from elasticsearch import Elasticsearch, RequestsHttpConnection

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

ELASTIC_PORT = os.environ.get("ELASTIC_PORT", None)
ELASTIC_USERNAME = os.environ.get("ELASTIC_USERNAME", None)
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD", None)

assert ELASTIC_PORT is not None, "ELASTIC_PORT is not set"
assert ELASTIC_USERNAME is not None, "ELASTIC_USERNAME is not set"
assert ELASTIC_PASSWORD is not None, "ELASTIC_PASSWORD is not set"

def test_es_connection():
    es = Elasticsearch([f'http://0.0.0.0:{ELASTIC_PORT}'],
                        timeout=100, \
                        connection_class=RequestsHttpConnection, 
                        http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD), 
                        use_ssl=False, 
                        verify_certs=False)
    
    assert es.ping() == True, "Elasticsearch is not running"