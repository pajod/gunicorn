from typing import TypeAlias

from _typeshed import Incomplete

_t_peer: TypeAlias = tuple[str, int] | str

class UWSGIParseException(Exception): ...

class InvalidUWSGIHeader(UWSGIParseException):
    msg: str
    code: int
    def __init__(self, msg: str = "") -> None: ...

class UnsupportedModifier(UWSGIParseException):
    modifier: bytes
    code: int
    def __init__(self, modifier: bytes) -> None: ...

class ForbiddenUWSGIRequest(UWSGIParseException):
    host: _t_peer
    code: int
    def __init__(self, host: _t_peer) -> None: ...
