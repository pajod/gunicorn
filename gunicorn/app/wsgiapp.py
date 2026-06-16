#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

from gunicorn.errors import ConfigError
from gunicorn.app.base import Application
from gunicorn import util


class WSGIApplication(Application):
    def init(self, parser, opts, args):
        self.app_uri = None

        if opts.paste:
            raise NotImplementedError("Feature removed from this unmaintained fork.")

        if len(args) > 0:
            self.cfg.set("default_proc_name", args[0])
            self.app_uri = args[0]

    def load_config(self):
        super().load_config()

        if self.app_uri is None:
            if self.cfg.wsgi_app is not None:
                self.app_uri = self.cfg.wsgi_app
            else:
                raise ConfigError("No application module specified.")

    def load_wsgiapp(self):
        return util.import_app(self.app_uri)

    def load(self):
        return self.load_wsgiapp()


def run(prog=None):
    """\
    The ``gunicorn`` command line runner for launching Gunicorn with
    generic WSGI applications.
    """
    from gunicorn.app.wsgiapp import WSGIApplication
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]", prog=prog).run()


if __name__ == '__main__':
    run()
