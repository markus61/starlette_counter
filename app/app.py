from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Route

cs = {}

class Counters(HTTPEndpoint):
    async def get(self, request):
        counter_name = request.path_params['counter']
        if counter_name not in cs:
            cs[counter_name] = 0
        return PlainTextResponse(f"Value of '{counter_name}' is: {cs[counter_name]}")

    async def post(self, request):
        counter_name = request.path_params['counter']
        if counter_name not in cs:
            cs[counter_name] = 0
        cs[counter_name] += 1
        return PlainTextResponse()
routes = [    
    Route("/{counter}", Counters)
]

app = Starlette(routes=routes)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="*", port=5000, log_level="debug")