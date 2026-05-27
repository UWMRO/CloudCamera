import logging
import asyncio
import inspect
import http


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)


class ConnectionHandler(asyncio.Protocol):
    transport: asyncio.WriteTransport | None = None

    def __init__(self, routes: dict[str, function]):
        self.routes = routes
        self.buffer = bytearray()
        self. logger = logging.getLogger(__name__)

    def connection_made(self, transport: asyncio.BaseTransport):
        self.transport = transport

    def data_received(self, data: bytes):
        self.buffer.extend(data)

        request_headers_index = self.buffer.find(b'\r\n\r\n')
        if request_headers_index == -1:
            return

        request_headers = self.buffer[:request_headers_index].decode(
            errors='ignore')
        request = ConnectionHandler.parse_request(request_headers)
        self.logger.info(
            f"{request.get('method')} {request.get('path')} - {request.get('User-Agent')}")

        if request['method'] != 'GET':
            response_coro = self.send_response(
                405, "<h1>405 Method Not Allowed</h1>")
        elif request['path'] not in self.routes:
            response_coro = self.send_response(
                404, "<h1>404 Not Found</h1>\n<a href=\"/home\">Back to Home</a>")
        else:
            handler = self.routes[request['path']]
            response_coro = self.send_response(200, handler)

        asyncio.create_task(response_coro)

    @staticmethod
    def parse_request(header_data: str):
        request = {}

        lines = header_data.split('\r\n')

        request_line = lines[0]
        method, path, _ = request_line.split()
        request['method'] = method
        request['path'] = path

        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', maxsplit=1)
                request[key.strip()] = value.strip()

        return request

    async def send_response(self, status_code: int, content: str | function):
        if inspect.iscoroutinefunction(content):
            body = await content()
        else:
            body = content

        response = (
            f"HTTP/1.1 {status_code} {http.HTTPStatus(status_code).phrase}\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
            f"{body}"
        )

        self.transport.write(response.encode())
        self.transport.close()
