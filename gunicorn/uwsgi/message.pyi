from _typeshed import Incomplete

from gunicorn._protocol import ParserProtocol
from gunicorn._type import _t_peer
from gunicorn.http.body import Body as Body
from gunicorn.http.body import LengthReader as LengthReader
from gunicorn.http.unreader import Unreader
from gunicorn.uwsgi.errors import ForbiddenUWSGIRequest as ForbiddenUWSGIRequest
from gunicorn.uwsgi.errors import InvalidUWSGIHeader as InvalidUWSGIHeader
from gunicorn.uwsgi.errors import UnsupportedModifier as UnsupportedModifier

MAX_UWSGI_VARS: int

from typing import Literal

from _typeshed import Incomplete

from gunicorn._type import _t_peer
from gunicorn.config import Config
from gunicorn.http.body import Body
from gunicorn.http.body import Body as Body
from gunicorn.http.body import ChunkedReader, EOFReader
from gunicorn.http.body import LengthReader
from gunicorn.http.body import LengthReader as LengthReader
from gunicorn.http.unreader import Unreader

class UWSGIRequest(ParserProtocol):

    cfg: Config
    unreader: Unreader
    peer_addr: _t_peer
    remote_addr: _t_peer

    req_number: Incomplete
    method: Incomplete
    uri: Incomplete
    path: Incomplete
    query: Incomplete
    fragment: str
    version: tuple[int, int]
    headers: list[tuple[str, str]]
    trailers: list[tuple[str, str]]
    body: Body | None
    scheme: Literal["https", "http"]
    must_close: bool
    uwsgi_vars: Incomplete
    modifier1: int
    modifier2: int
    proxy_protocol_info: Incomplete
    def __init__(
        self, cfg: Config, unreader: Unreader, peer_addr: _t_peer, req_number: int = 1
    ) -> None: ...
    def force_close(self) -> None: ...
    def parse(self, unreader: Unreader) -> None: ...
    def set_body_reader(self) -> None: ...
    def should_close(self) -> bool: ...
