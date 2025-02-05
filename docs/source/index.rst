======================
Gunicorn - WSGI server
======================

.. image:: _static/gunicorn.png

:Website: https://gunicorn.org
:Source code: https://github.com/benoitc/gunicorn
:Issue tracker: https://github.com/benoitc/gunicorn/issues
:IRC: ``#gunicorn`` on Libera Chat
:Usage questions: https://github.com/benoitc/gunicorn/issues

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork
worker model ported from Ruby's Unicorn project. The Gunicorn server is broadly
compatible with various web frameworks, simply implemented, light on server
resources, and fairly speedy.

Features
--------

* Natively supports WSGI, Django, and Paster
* Automatic worker process management
* Simple Python configuration
* Multiple worker configurations
* Various server hooks for extensibility
* Compatible with Python 3.x >= 3.7


Contents
--------

.. toctree::
    :maxdepth: 2

    install
    run
    configure
    settings
    instrumentation
    deploy
    signals
    custom
    design
    faq
    community
    news


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
