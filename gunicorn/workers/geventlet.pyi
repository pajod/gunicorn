from contextlib import AbstractAsyncContextManager
from signal import Signals
from socket import socket
from types import FrameType
from typing import TYPE_CHECKING, TypeAlias

import eventlet  # type: ignore[import-untyped]
from _typeshed import Incomplete

from gunicorn.http.message import Message
from gunicorn.workers.base import Worker
from gunicorn.workers.base_async import AsyncWorker

_t_peer_addr: TypeAlias = tuple[str, int] | str

EVENTLET_WSGI_LOCAL: Incomplete
EVENTLET_ALREADY_HANDLED: Incomplete

def patch_sendfile() -> None: ...

class EventletWorker(AsyncWorker):
    def patch(self) -> None: ...
    def is_already_handled(self, respiter: Incomplete) -> bool: ...
    def init_process(self) -> None: ...
    def handle_quit(self, sig: Signals, frame: FrameType | None) -> None: ...
    def handle_usr1(self, sig: Signals, frame: FrameType | None) -> None: ...
    def timeout_ctx(self) -> AbstractAsyncContextManager[None]: ...
    def handle(self, listener: socket, client: socket, addr: _t_peer_addr) -> None: ...
    def run(self) -> None: ...
