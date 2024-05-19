from signal import Signals
from types import FrameType

from _typeshed import Incomplete

from gunicorn.workers.base import Worker

TORNADO5: bool

class TornadoResponse:
    status: str
    headers: list[tuple[str, str]]
    sent: int

    def __init__(self, status: str, headers: list[tuple[str, str]], clength: int): ...

class TornadoWorker(Worker):
    @classmethod
    def setup(cls) -> None: ...
    def handle_exit(self, sig: Signals, frame: FrameType | None) -> None: ...
    alive: bool
    def handle_request(self) -> None: ...
    def watchdog(self) -> None: ...
    server_alive: bool
    def heartbeat(self) -> None: ...
    def init_process(self) -> None: ...
    ioloop: Incomplete
    callbacks: Incomplete
    server: Incomplete
    def run(self) -> None: ...
