import io
from collections.abc import Callable, Sequence
from logging import Logger
from re import Pattern

from _typeshed import Incomplete, OptExcInfo
from _typeshed.wsgi import StartResponse, WSGIEnvironment
from typing_extensions import Never

from gunicorn import SERVER as SERVER
from gunicorn import SERVER_SOFTWARE as SERVER_SOFTWARE
from gunicorn.config import Config
from gunicorn.http.message import Message

BLKSIZE: int
HEADER_VALUE_RE: Pattern[str]
log: Logger

class FileWrapper:
    filelike: Incomplete
    blksize: int
    close: Callable[[], None]
    def __init__(self, filelike: Incomplete, blksize: int = ...) -> None: ...
    def __getitem__(self, key: Never) -> Incomplete: ...

class WSGIErrorsWrapper(io.RawIOBase):
    streams: Incomplete
    def __init__(self, cfg: Config) -> None: ...
    def write(self, data: Incomplete) -> None: ...

def base_environ(cfg: Config) -> WSGIEnvironment: ...
def default_environ(req: Message, sock: Incomplete, cfg: Config) -> WSGIEnvironment: ...
def proxy_environ(req: Message) -> WSGIEnvironment: ...
def create(
    req: Message, sock: Incomplete, client: Incomplete, server: Incomplete, cfg: Config
) -> tuple[Response, WSGIEnvironment]: ...

class Response:
    req: Message
    sock: Incomplete
    version: str
    status: str
    chunked: bool
    must_close: bool
    headers: list[tuple[str, str]]
    headers_sent: bool
    response_length: None | int
    sent: int
    upgrade: bool
    cfg: Config
    def __init__(self, req: Message, sock: Incomplete, cfg: Config) -> None: ...
    def force_close(self) -> None: ...
    def should_close(self) -> bool: ...
    status_code: int
    # start_response: StartResponse
    def start_response(
        self,
        status: str,
        headers: list[tuple[str, str]],
        exc_info: OptExcInfo | None = None,
    ) -> Callable[[bytes], Incomplete]: ...
    def process_headers(self, headers: Sequence[tuple[str, str]]) -> None: ...
    def is_chunked(self) -> bool: ...
    def default_headers(self) -> Incomplete: ...
    def send_headers(self) -> None: ...
    def write(self, arg: bytes) -> None: ...
    def can_sendfile(self) -> bool: ...
    def sendfile(self, respiter: Incomplete) -> Incomplete: ...
    def write_file(self, respiter: Incomplete) -> None: ...
    def close(self) -> None: ...
