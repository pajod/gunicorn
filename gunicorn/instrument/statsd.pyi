import socket
from collections.abc import Mapping
from datetime import timedelta
from typing import Any, Literal

from _typeshed import Incomplete

from gunicorn.config import Config
from gunicorn.glogging import Logger as Logger
from gunicorn.http.message import Message
from gunicorn.http.wsgi import Response

METRIC_VAR: str
VALUE_VAR: str
MTYPE_VAR: str
GAUGE_TYPE: str
COUNTER_TYPE: str
HISTOGRAM_TYPE: str

class Statsd(Logger):
    prefix: str
    sock: socket.socket | None
    dogstatsd_tags: Incomplete
    def __init__(self, cfg: Config) -> None: ...
    def critical(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None: ...
    def error(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None: ...
    def warning(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None: ...
    def info(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None: ...
    def debug(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None: ...
    def exception(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None: ...
    def log(self, lvl: str, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None: ...
    def access(
        self,
        resp: Response,
        req: Message,
        environ: Mapping[str, str],
        request_time: timedelta,
    ) -> None: ...
    def gauge(self, name: str, value: int) -> None: ...
    def increment(self, name: str, value: int, sampling_rate: float = ...) -> None: ...
    def decrement(self, name: str, value: int, sampling_rate: float = ...) -> None: ...
    def histogram(self, name: str, value: int) -> None: ...
    def _sock_send(self, msg: str) -> None: ...
