import os
from dotenv import load_dotenv
from pathlib import Path
from milvus import Milvus

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

MILVUS_PORT = os.environ.get("MILVUS_PORT", None)

assert MILVUS_PORT is not None, "MILVUS_PORT is not set"

def test_milvus_connection():
    client = Milvus(host='localhost', port=MILVUS_PORT)
