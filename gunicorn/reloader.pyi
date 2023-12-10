import threading

from _typeshed import Incomplete

COMPILED_EXT_RE: Incomplete

class Reloader(threading.Thread):
    daemon: bool
    def __init__(
        self,
        extra_files: Incomplete | None = ...,
        interval: int = ...,
        callback: Incomplete | None = ...,
    ) -> None: ...
    def add_extra_file(self, filename) -> None: ...
    def get_files(self): ...
    def run(self) -> None: ...

has_inotify: bool

# ignoring duplicate - that one is guaranteed to error on actual use
class InotifyReloader(threading.Thread):
    event_mask: Incomplete
    daemon: bool
    def __init__(self, extra_files: Incomplete | None = ..., callback: Incomplete | None = ...) -> None: ...
    def add_extra_file(self, filename) -> None: ...
    def get_dirs(self): ...
    def run(self) -> None: ...

preferred_reloader: Incomplete
reloader_engines: Incomplete
