from typing import TYPE_CHECKING, Literal, Protocol

from _typeshed import Incomplete

from gunicorn.config import Config
from gunicorn.http.body import Body
from gunicorn.http.unreader import Unreader

if TYPE_CHECKING:
    from gunicorn._type import _t_peer

class ParserProtocol(Protocol):
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
    proxy_protocol_info: Incomplete

    def __init__(
        self,
        cfg: Config,
        unreader: Unreader,
        peer_addr: _t_peer,
        req_number: int = 1,
    ) -> None: ...
    def set_body_reader(self) -> None: ...
    def should_close(self) -> bool: ...
    def force_close(self) -> None: ...
    def parse(self, unreader: Unreader) -> None: ...
