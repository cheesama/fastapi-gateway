from fastapi import FastAPI, Depends, Header, WebSocket
from fastapi.routing import APIRoute
from fastapi.responses import HTMLResponse
from fastapi.concurrency import run_in_threadpool
from httpx import AsyncClient

app = FastAPI()
 
@app.get('/test1/{param_1}/{param_2}')
async def call__test1__param_1___param_2_(param_1,param_2,):
    async with AsyncClient() as client: 
        res = await client.get('http://localhost:1337/api/services')
        return res.json()
 
@app.get('/test2')
async def call__test2():
    async with AsyncClient() as client: 
        res = await client.get('http://localhost:1337/api/products')
        return res.json()
