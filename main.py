from fastapi import FastAPI

import json
import httpx
import asyncio

app = FastAPI()

with open("config.json", "r") as configFile:
    config = json.load(configFile)

for route_info in config["routes"]:
    app.add_api_route(
        path=route_info["route"], endpoint=None, methods=route_info["method"]
    )
