from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from fastapi.responses import HTMLResponse
from fastapi.concurrency import run_in_threadpool
from httpx import AsyncClient

import jsonpatch

app = FastAPI()

#httpx not follow redirects by default.

{% for route in routes %} 
@app.{{route['method'].lower()}}('{{route["route"]}}')
async def call_{{route["route"].replace('/','_').replace('{','_').replace('}','_')}}(
    {%- for param in route["route"].split('{') if '}' in param -%}
    {{param.replace('}','').replace('/','')}},
    {%- endfor -%}request: Request):
    headers = request.headers
    body = request.body
    async with AsyncClient() as client:
    {%- for backend in route['backends'] %} 
        response = await client.{{backend['method'].lower()}}(f'{{backend["host"]}}{{backend["url"]}}')
        if  not response.is_success:
            print ('not success!')
            return response.json()

        headers = response.headers
        body = response.json()

        {%- if 'header_json_patch' in backend %}
        header_patch = jsonpatch.JsonPatch(backend['header_json_patch'])
        headers = header_patch.apply(headers)
        {% endif %}

        {%- if 'body_json_patch' in backend %}
        body_patch = jsonpatch.JsonPatch(backend['body_json_patch'])
        body = body_patch.apply(body)
        {% endif %}

    {% endfor %}
        return body
        

{% endfor %}