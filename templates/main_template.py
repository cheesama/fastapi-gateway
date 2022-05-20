from fastapi import FastAPI, Depends, Header, WebSocket
from fastapi.routing import APIRoute
from fastapi.responses import HTMLResponse
from fastapi.concurrency import run_in_threadpool
from httpx import AsyncClient

app = FastAPI()

{% for route in routes %} 
@app.{{route['method'].lower()}}('{{route["route"]}}')
async def call_{{route["route"].replace('/','_').replace('{','_').replace('}','_')}}(
    {%- for param in route["route"].split('{') if '}' in param -%}
    {{param.replace('}','').replace('/','')}},
    {%- endfor -%}):
    async with AsyncClient() as client:
    {%- for backend in route['backends'] %} 
        res = await client.{{backend['method'].lower()}}('{{backend["host"]}}{{backend["url"]}}')
        return res.json()
    {% endfor -%}
{% endfor %}