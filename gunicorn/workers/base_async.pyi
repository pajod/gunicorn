from _typeshed import Incomplete

from gunicorn import http as http
from gunicorn import util as util
from gunicorn.http import wsgi as wsgi
from gunicorn.workers import base as base

ALREADY_HANDLED: Incomplete

class AsyncWorker(base.Worker):
    worker_connections: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def timeout_ctx(self) -> None: ...
    def is_already_handled(self, respiter): ...
    def handle(self, listener, client, addr) -> None: ...
    alive: bool
    def handle_request(self, listener_name, req, sock, addr): ...
