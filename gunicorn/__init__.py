#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

version_info = (26, 0, 0)
local_suffix = "+unmaintained0"
__version__ = ".".join([str(v) for v in version_info]) + local_suffix
SERVER = "gunicorn"
SERVER_SOFTWARE = "%s/%s" % (SERVER, __version__)

__all__ = [
    "__version__",
    "SERVER",
    "SERVER_SOFTWARE",
]
