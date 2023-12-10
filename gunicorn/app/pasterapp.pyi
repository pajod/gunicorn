from _typeshed import Incomplete

from gunicorn.app.wsgiapp import WSGIApplication as WSGIApplication
from gunicorn.config import get_default_config_file as get_default_config_file

def get_wsgi_app(config_uri, name: Incomplete | None = ..., defaults: Incomplete | None = ...): ...
def has_logging_config(config_file): ...
def serve(app, global_conf, **local_conf): ...
