from _typeshed import Incomplete

from gunicorn.http.message import Message

class ParseException(Exception):
    code: int
    reason: str

class NoMoreData(IOError):
    buf: Incomplete
    def __init__(self, buf: bytes | None = None) -> None: ...

class ConfigurationProblem(ParseException):
    info: str
    code: int
    def __init__(self, info: str) -> None: ...

class ExpectationFailed(ParseException):
    expect: str
    def __init__(self, expect: str) -> None: ...

class InvalidRequestLine(ParseException):
    req: str
    def __init__(self, req: str) -> None: ...

class InvalidRequestMethod(ParseException):
    method: str
    def __init__(self, method: str) -> None: ...

class InvalidHTTPVersion(ParseException):
    version: str
    def __init__(self, version: str) -> None: ...

class InvalidHeader(ParseException):
    hdr: str
    req: Message | None
    def __init__(self, hdr: str, req: Message | None = ...) -> None: ...

class IncompleteBody(ParseException): ...

class ObsoleteFolding(ParseException):
    hdr: str
    def __init__(self, hdr: str): ...

class InvalidHeaderName(ParseException):
    hdr: str
    def __init__(self, hdr: str) -> None: ...

class UnsupportedTransferCoding(ParseException):
    hdr: str
    def __init__(self, hdr: str) -> None: ...

class InvalidChunkSize(IOError):
    data: bytes
    def __init__(self, data: bytes) -> None: ...

class ChunkMissingTerminator(IOError):
    term: bytes
    def __init__(self, term: bytes) -> None: ...

class LimitRequestLine(ParseException):
    size: int
    max_size: int
    def __init__(self, size: int, max_size: int) -> None: ...

class LimitRequestHeaders(ParseException):
    msg: str
    def __init__(self, msg: str) -> None: ...

class InvalidProxyLine(ParseException):
    line: str
    def __init__(self, line: str) -> None: ...

class ForbiddenProxyRequest(ParseException):
    host: str
    def __init__(self, host: str) -> None: ...

class InvalidSchemeHeaders(ParseException): ...
