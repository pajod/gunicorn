from re import Pattern
from typing import TYPE_CHECKING, BinaryIO, Literal, TypeAlias

from _typeshed import Incomplete

from gunicorn.http.body import Body, ChunkedReader, EOFReader, LengthReader
from gunicorn.http.errors import (
    ForbiddenProxyRequest,
    InvalidHeader,
    InvalidHeaderName,
    InvalidHTTPVersion,
    InvalidProxyLine,
    InvalidRequestLine,
    InvalidRequestMethod,
    InvalidSchemeHeaders,
    LimitRequestHeaders,
    LimitRequestLine,
    NoMoreData,
)
from gunicorn.http.unreader import Unreader

if TYPE_CHECKING:
    from gunicorn.config import Config

MAX_REQUEST_LINE: int
MAX_HEADERS: int
DEFAULT_MAX_HEADERFIELD_SIZE: int

RFC9110_5_6_2_TOKEN_SPECIALS: str
TOKEN_RE: Pattern[str]
METHOD_BADCHAR_RE: Pattern[str]
VERSION_RE: Pattern[str]

_t_peer: TypeAlias = tuple[str, int] | str

class Message:
    cfg: Config
    unreader: Unreader
    peer_addr: _t_peer
    remote_addr: _t_peer
    version: tuple[int, int]
    headers: list[tuple[str, str]]
    trailers: list[tuple[str, str]]
    body: Body | None
    scheme: Literal["https", "http"]
    must_close: bool
    limit_request_fields: Incomplete
    limit_request_field_size: Incomplete
    max_buffer_headers: Incomplete
    def __init__(self, cfg: Config, unreader: Unreader, peer_addr: _t_peer) -> None: ...
    def force_close(self) -> None: ...
    def parse(self, unreader: Unreader) -> None: ...
    def parse_headers(self, data: bytes, from_trailer: bool = False) -> Incomplete: ...
    def set_body_reader(self) -> None: ...
    def should_close(self) -> bool: ...

class Request(Message):
    method: Incomplete
    uri: Incomplete
    path: Incomplete
    query: Incomplete
    fragment: Incomplete
    limit_request_line: Incomplete
    req_number: Incomplete
    proxy_protocol_info: Incomplete
    def __init__(
        self,
        cfg: Config,
        unreader: Unreader,
        peer_addr: _t_peer,
        req_number: int = 1,
    ) -> None: ...
    def get_data(
        self, unreader: Config, buf: BinaryIO, stop: bool = ...
    ) -> Incomplete: ...
    headers: Incomplete
    def read_line(
        self, unreader: Unreader, buf: BinaryIO, limit: int = ...
    ) -> Incomplete: ...
    def proxy_protocol(self, line: str) -> Incomplete: ...
    def proxy_protocol_access_check(self) -> None: ...
    def parse_proxy_protocol(self, line: str) -> None: ...
    def parse_request_line(self, line_bytes: bytes) -> None: ...
    def set_body_reader(self) -> None: ...
