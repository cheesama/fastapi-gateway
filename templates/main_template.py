from fastapi import FastAPI, Header, WebSocket
from fastapi.routing import APIRoute
from fastapi.responses import HTMLResponse
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, AnyUrl
from enum import Enum
from typing import List, Dict

import requests

class MethodEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    UPDATE = "UPDATE"
    PATCH = "PATCH"

class BackendInfo(BaseModel):
    url: AnyUrl
    method: MethodEnum
    header_json_patch: Dict = None
    body_json_patch: Dict = None

class RouteInfo(BaseModel):
    route: str
    method: MethodEnum
    backends: List[BackendInfo]

class GlobalConfig(BaseModel):
    port: int
    routes: List[RouteInfo]

app = FastAPI()

{% for route in routes %} 
@app.{{route['method'].lower()}}('{{route["route"]}}')
async def call_{{route["route"].replace('/','_').replace('{','_').replace('}','_')}}(
    {%- for param in route["route"].split('{') if '}' in param -%}
    {{param.replace('}','').replace('/','')}},
    {%- endfor -%}
)
    {%- for backend in route['backends'] %} 
    res = await requests.{{backend['method'].lower()}}('{{backend["host"]}}{{backend["url"]}}')
    {% endfor -%}
{% endfor %}