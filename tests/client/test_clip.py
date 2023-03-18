import requests
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

CLIP_PORT = os.environ.get("CLIP_PORT", None)

assert CLIP_PORT is not None, "CLIP_PORT is not set"

def test_text_encode(text = "a funny man with a hat"):
    api = f"api/text/{text}"
    url = f"http://localhost:{CLIP_PORT}/{api}"
    response = requests.get(url)
    assert response.status_code == 200
    response = response.json() 
    assert response['feature'] is not None

def test_encode_image(image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png"):
    api = f"api/image"
    url = f"http://localhost:{CLIP_PORT}/{api}"
    response = requests.post(url, json={"url": image_url})
    assert response.status_code == 201, f"Request on {url} failed"

    response = response.json() 
    assert response['feature'] is not None

print(CLIP_PORT)
# test_encode_image()
test_text_encode()