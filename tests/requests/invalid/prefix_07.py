from gunicorn.config import Config
from gunicorn.http.errors import InvalidRequestLine

cfg = Config()
request = InvalidRequestLine
