from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from fastapi.responses import HTMLResponse
from fastapi.concurrency import run_in_threadpool
from httpx import AsyncClient

import jsonpatch

app = FastAPI()

#httpx not follow redirects by default.

 
@app.get('/test1/{param_1}/{param_2}')
async def call__test1__param_1___param_2_(param_1,param_2,request: Request):
    headers = request.headers
    body = request.body
    async with AsyncClient() as client: 
        response = await client.get(f'http://localhost:1337/api/services')
        if  not response.is_success:
            print ('not success!')
            return response.json()

        headers = response.headers
        body = response.json()

 
        response = await client.get(f'http://localhost:1337/api/products')
        if  not response.is_success:
            print ('not success!')
            return response.json()

        headers = response.headers
        body = response.json()


        return body
        

 
@app.get('/test2')
async def call__test2(request: Request):
    headers = request.headers
    body = request.body
    async with AsyncClient() as client: 
        response = await client.get(f'http://localhost:1337/api/products')
        if  not response.is_success:
            print ('not success!')
            return response.json()

        headers = response.headers
        body = response.json()


        return body
        

