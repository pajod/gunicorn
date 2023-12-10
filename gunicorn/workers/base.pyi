from typing import List

from _typeshed import Incomplete

from gunicorn import util as util
from gunicorn.app.wsgiapp import WSGIApplication as WSGIApplication
from gunicorn.config import Config as Config
from gunicorn.glogging import Logger as Logger
from gunicorn.http.errors import ForbiddenProxyRequest as ForbiddenProxyRequest
from gunicorn.http.errors import InvalidHeader as InvalidHeader
from gunicorn.http.errors import InvalidHeaderName as InvalidHeaderName
from gunicorn.http.errors import InvalidHTTPVersion as InvalidHTTPVersion
from gunicorn.http.errors import InvalidProxyLine as InvalidProxyLine
from gunicorn.http.errors import InvalidRequestLine as InvalidRequestLine
from gunicorn.http.errors import InvalidRequestMethod as InvalidRequestMethod
from gunicorn.http.errors import InvalidSchemeHeaders as InvalidSchemeHeaders
from gunicorn.http.errors import LimitRequestHeaders as LimitRequestHeaders
from gunicorn.http.errors import LimitRequestLine as LimitRequestLine
from gunicorn.http.wsgi import Response as Response
from gunicorn.http.wsgi import default_environ as default_environ
from gunicorn.reloader import reloader_engines as reloader_engines
from gunicorn.sock import TCPSocket as TCPSocket
from gunicorn.workers.workertmp import WorkerTmp as WorkerTmp

Pipe: Incomplete

class Worker:
    SIGNALS: Incomplete
    PIPE: list[Pipe]
    age: Incomplete
    pid: str
    ppid: Incomplete
    sockets: Incomplete
    app: Incomplete
    timeout: Incomplete
    cfg: Incomplete
    booted: bool
    aborted: bool
    reloader: Incomplete
    nr: int
    max_requests: Incomplete
    alive: bool
    log: Incomplete
    tmp: Incomplete
    def __init__(
        self,
        age: int,
        ppid: int,
        sockets: list[TCPSocket],
        app: WSGIApplication,
        timeout: float,
        cfg: Config,
        log: Logger,
    ) -> None: ...
    def notify(self) -> None: ...
    def run(self) -> None: ...
    wait_fds: Incomplete
    def init_process(self) -> None: ...
    wsgi: Incomplete
    def load_wsgi(self) -> None: ...
    def init_signals(self) -> None: ...
    def handle_usr1(self, sig, frame) -> None: ...
    def handle_exit(self, sig, frame) -> None: ...
    def handle_quit(self, sig, frame) -> None: ...
    def handle_abort(self, sig, frame) -> None: ...
    def handle_error(self, req, client, addr, exc) -> None: ...
    def handle_winch(self, sig, fname) -> None: ...
