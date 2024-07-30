from gunicorn.http.errors import ObsoleteFolding
from gunicorn.config import Config

cfg = Config()
cfg.set('refuse_obsolete_folding', True)

request = ObsoleteFolding
