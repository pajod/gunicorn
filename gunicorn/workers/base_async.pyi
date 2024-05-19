from contextlib import AbstractAsyncContextManager
from socket import socket
from typing import TypeAlias

from _typeshed import Incomplete

from gunicorn.http.message import Message
from gunicorn.workers.base import Worker

_t_ListenInfo: TypeAlias = tuple[str, int] | str | bytes
_t_peer_addr: TypeAlias = tuple[str, int] | str

ALREADY_HANDLED: object

class AsyncWorker(Worker):
    worker_connections: int
    def timeout_ctx(self) -> AbstractAsyncContextManager[None]: ...
    def is_already_handled(self, respiter: Incomplete) -> bool: ...
    def handle(self, listener: socket, client: socket, addr: _t_peer_addr) -> None: ...
    alive: bool
    def handle_request(
        self,
        listener_name: _t_ListenInfo,
        req: Message,
        sock: socket,
        addr: _t_peer_addr,
    ) -> bool | None: ...
