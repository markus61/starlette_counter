from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Route

from multiprocessing.managers import BaseManager

# Manager
class Client(BaseManager): pass
Client.register("Counter")

# Connects to a remote server.
client = Client(address=('', 55555), authkey=b"1Belgisches4tel23")
client.connect()
class Counters(HTTPEndpoint):
    async def get(self, request):
        counter_name = request.path_params['counter']
        counter = client.Counter(name=counter_name)
        return PlainTextResponse(str(counter.value()))

    async def post(self, request):
        counter_name = request.path_params['counter']
        counter = client.Counter(name=counter_name)
        body = await request.body()
        try:
            value = int(body.decode())
            counter.set(value)
        except ValueError:
            counter.increment()
        return PlainTextResponse()

routes = [    
    Route("/counters/{counter}", Counters)
]

app = Starlette(routes=routes)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="*", port=5000, log_level="debug")