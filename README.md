# fastapi-gateway

## config.json format

```json
{
  "port" : 80,
  "routes" : [
    "route" : "/",
    "backends": [
      {
        "url": "http://some-landing",
        "method": "GET",
        "header_json_patch" : [
          { "op": "add", "path": "/biscuits/1", "value": { "name": "Ginger Nut" } }
        ],
        "body_json_patch": [
          { "op": "test", "path": "/best_biscuit/name", "value": "Choco Leibniz" }
        ]
      }
    ]
  ]
}
```

```mermaid
  graph LR;
      A[config.json]-->B[parser]
      B-->|check route parts|C[generated route endpoints]
      B-->|checkt backend parts|D[generated backend endpoints]
     
```

```mermaid
  graph LR;
      A[user request]-->B(route endpoint 1)-->D([backend endpoint 1]);
      A-->C(route endpoint 2);
      A-->G(rount enpoint ...);
      G-->H([backend enpoint ...]);
      D-->|return transformation response|B
      C-->E([backend endpoint 2]);
      E-.->|return error response without forwarding next backend if request fail|C
      E-->|deliver reseponse after header / body json-patch operation|I([backend endpoint 3]);
      I-->|return merge & transformation response|C
```

## to-do
- check https://github.com/comeuplater/fastapi_cache for response caching
