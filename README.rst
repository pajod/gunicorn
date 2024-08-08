Gunicorn
--------

.. image:: https://img.shields.io/pypi/v/gunicorn.svg?style=flat
    :alt: PyPI version
    :target: https://pypi.python.org/pypi/gunicorn

.. image:: https://img.shields.io/pypi/pyversions/gunicorn.svg
    :alt: Supported Python versions
    :target: https://pypi.python.org/pypi/gunicorn

.. image:: https://github.com/benoitc/gunicorn/actions/workflows/tox.yml/badge.svg
    :alt: Build Status
    :target: https://github.com/benoitc/gunicorn/actions/workflows/tox.yml

.. image:: https://github.com/benoitc/gunicorn/actions/workflows/lint.yml/badge.svg
    :alt: Lint Status
    :target: https://github.com/benoitc/gunicorn/actions/workflows/lint.yml

Gunicorn 'Green Unicorn' is a Python WSGI_ HTTP Server for UNIX. It's a pre-fork
worker model ported from Ruby's Unicorn_ project. The Gunicorn server is broadly
compatible with various web frameworks, simply implemented, light on server
resource usage, and fairly speedy.

Feel free to join us in `#gunicorn`_ on `Libera.chat`_.

Documentation
-------------

The documentation is hosted at https://docs.gunicorn.org.

Installation
------------

Gunicorn requires **Python 3.x >= 3.7**.

Install from PyPI::

    $ pip install gunicorn


Usage
-----

Basic usage::

    $ gunicorn [OPTIONS] APP_MODULE

Where ``APP_MODULE`` is of the pattern ``$(MODULE_NAME):$(VARIABLE_NAME)``. The
module name can be a full dotted path. The variable name refers to a WSGI
callable that should be found in the specified module.

Example with test app::

    $ cd examples
    $ gunicorn --workers=2 test:app

Compatibility
-------------

Gunicorn understands HTTP/0.9, HTTP/1.0 and HTTP/1.1 and seeks to comply with the more recent
internet standards `RFC 9110: HTTP Semantics <https://datatracker.ietf.org/doc/html/rfc9110>`_ and
`RFC 9112: HTTP/1.1 <https://datatracker.ietf.org/doc/html/rfc9112>`_.


Gunicorn should work on any POSIX system running CPython or PyPy, however is only tested on some:

.. list-table:: Platforms
   :widths: 25 25 50
   :header-rows: 1

   * - Kernel / OS
     - Architectures
     - Notes
   * - Linux 3.2+
     - unicode:: arm64 (U+2705), x86_64 (U+2705), x86 (untested)
     - unicode:: CI-tested: Ubuntu (U+2705), Should work: almost any distribution
   * - Linux @ WSL2
     - x86_64
     - do not use Windows filesystems
   * - unicode:: x86_64 (U+270), arm64 (U+270)
     - unicode:: CI-tested: macOS 13 (U+270), macOS 14 (U+270)
     - performance issues in PyPy
   * - FreeBSD
     -
     - not CI-tested
   * - OpenBSD
     -
     - not CI-tested
   * - GNU Hurd
     - Guix System
     - unknown
   * - Windows
     - any
     - does not work (and even if non-portable code was updated, Windows PIPE handling was only completed in Python ``> 3.12``)

Gunicorn can be used with different workers, both included and externally provided.

.. list-table:: Worker compatiblity
   :widths: 50 50
   :header-rows: 1

   * - worker
     - notes
   * - sync
     - no pipe-lining support
   * - thread
     - always
   * - eventlet
     - greenlet, only Python ``< 3.13``, `*New usages of eventlet are now heavily discouraged!* <https://github.com/eventlet/eventlet?tab=readme-ov-file#warning>`_
   * - gevent
     - always
   * - tornado
     - always
   * - ``uvicorn.workers.UvicornWorker``, ``uvicorn.workers.UvicornH11Worker``
     - `deprecated <https://github.com/encode/uvicorn/pull/2302>`_
   * - uvicorn_worker.UvicornWorker
     - untested

Contributing
------------

See `our complete contributor's guide <CONTRIBUTING.md>`_ for more details.


License
-------

Gunicorn is released under the MIT License. See the LICENSE_ file for more
details.

Distributions
-------------

.. image:: https://repology.org/badge/vertical-allrepos/gunicorn.svg?minversion=21.1.0&columns=4&exclude_unsupported=1    :alt: Gunicorn is packaged in 28 repositories
    :target: https://repology.org/project/gunicorn/information

.. _Unicorn: https://bogomips.org/unicorn/
.. _`#gunicorn`: https://web.libera.chat/?channels=#gunicorn
.. _`Libera.chat`: https://libera.chat/
.. _LICENSE: https://github.com/benoitc/gunicorn/blob/master/LICENSE
.. _WSGI: https://peps.python.org/pep-0333/
