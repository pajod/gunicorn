from _typeshed import Incomplete

class HaltServer(BaseException):
    reason: Incomplete
    exit_status: Incomplete
    def __init__(self, reason: str, exit_status: int = ...) -> None: ...

class ConfigError(Exception): ...
class AppImportError(Exception): ...
