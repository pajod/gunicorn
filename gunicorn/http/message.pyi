from typing import BinaryIO

from _typeshed import Incomplete

from gunicorn.http.body import Body as Body
from gunicorn.http.body import ChunkedReader as ChunkedReader
from gunicorn.http.body import EOFReader as EOFReader
from gunicorn.http.body import LengthReader as LengthReader
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
from gunicorn.http.errors import NoMoreData as NoMoreData
from gunicorn.util import bytes_to_str as bytes_to_str
from gunicorn.util import split_request_uri as split_request_uri

MAX_REQUEST_LINE: int
MAX_HEADERS: int
DEFAULT_MAX_HEADERFIELD_SIZE: int
HEADER_RE: Incomplete
METH_RE: Incomplete
VERSION_RE: Incomplete

class Message:
    cfg: Incomplete
    unreader: Incomplete
    peer_addr: Incomplete
    remote_addr: Incomplete
    version: Incomplete
    headers: Incomplete
    trailers: Incomplete
    body: Incomplete
    scheme: Incomplete
    limit_request_fields: Incomplete
    limit_request_field_size: Incomplete
    max_buffer_headers: Incomplete
    def __init__(self, cfg, unreader, peer_addr) -> None: ...
    def parse(self, unreader) -> None: ...
    def parse_headers(self, data): ...
    def set_body_reader(self) -> None: ...
    def should_close(self): ...

class Request(Message):
    method: Incomplete
    uri: Incomplete
    path: Incomplete
    query: Incomplete
    fragment: Incomplete
    limit_request_line: Incomplete
    req_number: Incomplete
    proxy_protocol_info: Incomplete
    def __init__(self, cfg, unreader, peer_addr, req_number: int = ...) -> None: ...
    def get_data(self, unreader, buf: BinaryIO, stop: bool = ...): ...
    headers: Incomplete
    def parse(self, unreader): ...
    def read_line(self, unreader, buf, limit: int = ...): ...
    def proxy_protocol(self, line): ...
    def proxy_protocol_access_check(self) -> None: ...
    def parse_proxy_protocol(self, line) -> None: ...
    version: Incomplete
    def parse_request_line(self, line_bytes) -> None: ...
    body: Incomplete
    def set_body_reader(self) -> None: ...
