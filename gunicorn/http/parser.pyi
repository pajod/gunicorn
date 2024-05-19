from typing import TYPE_CHECKING

from _typeshed import Incomplete
from typing_extensions import Self

from gunicorn.http.message import Request
from gunicorn.http.unreader import IterUnreader, SocketUnreader

if TYPE_CHECKING:
    from gunicorn.config import Config

class Parser:
    mesg_class: type[Request] | None
    cfg: Incomplete
    unreader: Incomplete
    mesg: Incomplete
    source_addr: Incomplete
    req_count: int
    def __init__(self, cfg: Config, source: str, source_addr: str) -> None: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> Request: ...
    next = __next__

class RequestParser(Parser):
    mesg_class: type[Request] = Request
