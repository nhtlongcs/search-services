import os
from typing import Any, List, Optional, Union

import openai
from dotenv import load_dotenv
from starlite import Starlite, get, post
from schema.dtypes import RequestModel, ResponseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

import asyncio
from typing import Dict

from features.abductive import AbductiveChain



@get("/")
def read_root() -> Dict[str, str]:
    return {"API Name": "Prompt Completion API", "Version": "0.0.0"}


@post("/api/abductive/")
async def abductive_api(data: RequestModel) -> List[str]:
    text = data.text
    timeout = data.timeout
    ansync_result = await asyncio.wait_for(AbductiveChain().execute_wo_rate_limit(text), timeout=timeout)
    return ansync_result


app = Starlite(route_handlers=[read_root, abductive_api])
