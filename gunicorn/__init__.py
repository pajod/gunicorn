#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

version_info = (23, 1, 0)
__version__ = ".".join([str(v) for v in version_info]) + "a1"
SERVER = "gunicorn"
SERVER_SOFTWARE = "%s/%s" % (SERVER, __version__)
