from gc import callbacks
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, AnyUrl
from enum import Enum
from typing import List, Dict
from starlette.responses import JSONResponse

import uvicorn
import json
import aiohttp
import asyncio
import jsonpatch
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


routes = []



class BackendAggregator:
    def __init__(self, routeInfo: RouteInfo):
        self.backends = routeInfo.backends

    async def __call__(self):
        return await http_client.get(self.backends[0].url).json()

with open("config.json", "r") as configFile:
    config = GlobalConfig(**json.load(configFile))
    # print(config)

    for route_info in config.routes:
        backend_aggregator = BackendAggregator(route_info)
        routes.append(
            APIRoute(
                route_info.route,
                backend_aggregator,
                methods=[route_info.method],
                response_class=JSONResponse,
            )
        )

app = FastAPI(routes=routes)

class HttpClient:
    session: aiohttp.ClientSession = None

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    def __call__(self) -> aiohttp.ClientSession:
        assert self.session is not None
        return self.session

http_client = HttpClient()

@app.on_event("startup")
async def startup():
    http_client.start()



if __name__ == "__main__":  # local dev
    uvicorn.run(app, host="0.0.0.0", port=8000)
