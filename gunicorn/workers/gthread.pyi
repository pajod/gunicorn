from collections import deque
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from selectors import BaseSelector
from signal import Signals
from socket import socket
from types import FrameType
from typing import Type, TypeAlias

from _typeshed import Incomplete
from typing_extensions import Self

from gunicorn.config import Config
from gunicorn.glogging import Logger
from gunicorn.http.message import Message

from .base import Worker

_t_peer: TypeAlias = tuple[str, int] | str | bytes
_future_sig = Callable[[socket], tuple[bool, socket]]

class TConn:
    cfg: Incomplete
    sock: Incomplete
    client: Incomplete
    server: Incomplete
    timeout: Incomplete
    parser: Incomplete
    initialized: bool
    def __init__(
        self, cfg: Config, sock: socket, client: _t_peer, server: _t_peer
    ) -> None: ...
    def init(self) -> None: ...
    def set_timeout(self) -> None: ...
    def close(self) -> None: ...

class ThreadWorker(Worker):
    worker_connections: Incomplete
    max_keepalived: int
    tpool: ThreadPoolExecutor
    poller: BaseSelector
    futures: deque[Future[_future_sig]]
    _keep: deque[socket]
    nr_conns: int
    @classmethod
    def check_config(cls: type[Self], cfg: Config, log: Logger) -> None: ...
    def init_process(self) -> None: ...
    def get_thread_pool(self) -> ThreadPoolExecutor: ...
    alive: bool
    def handle_quit(self, sig: Signals, frame: FrameType | None) -> None: ...
    def _wrap_future(self, fs: Future[_future_sig], conn: socket) -> None: ...
    def enqueue_req(self, conn: socket) -> None: ...
    def accept(self, server: _t_peer, listener: socket) -> None: ...
    def on_client_socket_readable(self, conn: socket, client: _t_peer) -> None: ...
    def murder_keepalived(self) -> None: ...
    def is_parent_alive(self) -> bool: ...
    def run(self) -> None: ...
    def finish_request(self, fs: Future[_future_sig]) -> None: ...
    def handle(self, conn: socket) -> tuple[bool, socket]: ...
    def handle_request(self, req: Message, conn: socket) -> bool: ...
