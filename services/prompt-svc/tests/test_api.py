import os

from dotenv import load_dotenv; load_dotenv()
SVC_PORT = os.getenv("SVC_PORT")
import asyncio

import httpx


def test_get_svc_info():
    url = f"http://localhost:{SVC_PORT}/"
    async def get_api_info():
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            return resp.json()
        
    return asyncio.run(get_api_info())        

def test_abductive_chain_api(txt="I was praying to small golden Buddha in a tunnel."):
    
    api = f"api/abductive/"
    url = f"http://localhost:{SVC_PORT}/{api}"
    data = {"text": txt, "timeout": 20}
    async def get_abductive_chain_api(data):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url, json=data, timeout=data['timeout']
            )
            return resp
    resp = asyncio.run(get_abductive_chain_api(data))
    assert resp.status_code == 201, f"Request on {url} failed"
    return resp.json()

if __name__ == "__main__":
    print(test_get_svc_info())
    print(test_abductive_chain_api())