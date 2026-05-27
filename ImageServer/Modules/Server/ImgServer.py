import asyncio

from .ConnectionHandler import ConnectionHandler


class ImgServer:
    def __init__(self):
        self.routes: dict[str, function] = {}

    def route(self, endpoint: str):
        def decorator(func):
            self.routes[endpoint] = func
            return func
        return decorator

    def run(self):
        asyncio.run(self.serve())

    async def serve(self, port: int = 9999):
        loop = asyncio.get_running_loop()

        server = await loop.create_server(
            lambda: ConnectionHandler(self.routes),
            '127.0.0.1', port
        )

        async with server:
            await server.serve_forever()
