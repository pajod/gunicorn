from contextlib import AbstractAsyncContextManager
from signal import Signals
from socket import socket
from types import FrameType
from typing import Type, TypeAlias

import gevent  # type: ignore[import-untyped]
from _typeshed import Incomplete
from _typeshed.wsgi import StartResponse, WSGIEnvironment
from gevent import pywsgi

from gunicorn.http.message import Message
from gunicorn.workers.base_async import AsyncWorker

_t_ListenInfo: TypeAlias = tuple[str, int] | str | bytes
_t_peer_addr: TypeAlias = tuple[str, int] | str

VERSION: str

class GeventWorker(AsyncWorker):
    server_class: type[PyWSGIServer] | None
    wsgi_handler: type[PyWSGIHandler] | None
    sockets: Incomplete
    def patch(self) -> None: ...
    def notify(self) -> None: ...
    def timeout_ctx(self) -> AbstractAsyncContextManager[None]: ...
    def run(self) -> None: ...
    def handle(self, listener: socket, client: socket, addr: _t_peer_addr) -> None: ...
    def handle_request(
        self,
        listener_name: _t_ListenInfo,
        req: Message,
        sock: socket,
        addr: _t_peer_addr,
    ) -> None: ...
    def handle_quit(self, sig: Signals, frame: FrameType | None) -> None: ...
    def handle_usr1(self, sig: Signals, frame: FrameType | None) -> None: ...
    def init_process(self) -> None: ...

class GeventResponse:
    status: str
    headers: list[tuple[str, str]]
    sent: int
    def __init__(
        self, status: int, headers: list[tuple[str, str]], clength: int
    ) -> None: ...

class PyWSGIHandler(pywsgi.WSGIHandler):
    status: bytes | Incomplete
    response_headers: list[tuple[bytes, bytes]] | Incomplete

    def log_request(self) -> None: ...
    def get_environ(self) -> WSGIEnvironment: ...

class PyWSGIServer(pywsgi.WSGIServer): ...

class GeventPyWSGIWorker(GeventWorker):
    server_class: type[PyWSGIServer]
    wsgi_handler: type[PyWSGIHandler]
