from _typeshed import Incomplete

from .. import http as http
from .. import sock as sock
from .. import util as util
from ..http import wsgi as wsgi
from . import base as base

class TConn:
    cfg: Incomplete
    sock: Incomplete
    client: Incomplete
    server: Incomplete
    timeout: Incomplete
    parser: Incomplete
    initialized: bool
    def __init__(self, cfg, sock, client, server) -> None: ...
    def init(self) -> None: ...
    def set_timeout(self) -> None: ...
    def close(self) -> None: ...

class ThreadWorker(base.Worker):
    worker_connections: Incomplete
    max_keepalived: Incomplete
    tpool: Incomplete
    poller: Incomplete
    futures: Incomplete
    nr_conns: int
    def __init__(self, *args, **kwargs) -> None: ...
    @classmethod
    def check_config(cls, cfg, log) -> None: ...
    def init_process(self) -> None: ...
    def get_thread_pool(self): ...
    alive: bool
    def handle_quit(self, sig, frame) -> None: ...
    def enqueue_req(self, conn) -> None: ...
    def accept(self, server, listener) -> None: ...
    def on_client_socket_readable(self, conn, client) -> None: ...
    def murder_keepalived(self) -> None: ...
    def is_parent_alive(self): ...
    def run(self) -> None: ...
    def finish_request(self, fs) -> None: ...
    def handle(self, conn): ...
    def handle_request(self, req, conn): ...
