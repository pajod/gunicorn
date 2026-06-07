from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gunicorn.glogging import Logger

SD_LISTEN_FDS_START: int

def listen_fds(unset_environment: bool = ...) -> int: ...
def sd_notify(state: str, logger: Logger, unset_environment: bool = ...) -> None: ...
