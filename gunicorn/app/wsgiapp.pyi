from _typeshed import Incomplete

from gunicorn import util as util
from gunicorn.app.base import Application as Application
from gunicorn.errors import ConfigError as ConfigError

class WSGIApplication(Application):
    app_uri: Incomplete
    def init(self, parser, opts, args) -> None: ...
    def load_config(self) -> None: ...
    def load_wsgiapp(self): ...
    def load_pasteapp(self): ...
    def load(self): ...

def run() -> None: ...
