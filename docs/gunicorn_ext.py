import os
import inspect

from docutils import nodes, utils

from sphinx.parsers import RSTParser
from sphinx.util.nodes import split_explicit_title

import gunicorn.config as guncfg

HEAD = """\
.. Please update gunicorn/config.py instead.

.. _settings:

Settings
========

This is an exhaustive list of settings for Gunicorn. Some settings are only
able to be set from a configuration file. The setting name is what should be
used in the configuration file. The command line arguments are listed as well
for reference on setting at the command line.

.. note::

    Settings can be specified by using environment variable
    ``GUNICORN_CMD_ARGS``. All available command line arguments can be used.
    For example, to specify the bind address and number of workers::

        $ GUNICORN_CMD_ARGS="--bind=127.0.0.1 --workers=3" gunicorn app:app

    .. versionadded:: 19.7

"""
ISSUE_URI = 'https://github.com/benoitc/gunicorn/issues/%d'
PULL_REQUEST_URI = 'https://github.com/benoitc/gunicorn/pull/%d'


def format_settings(app):
    settings_file = os.path.join(app.srcdir, "settings.rst")
    with open(settings_file, 'w') as settings:
        settings.write(get_settings())
    app.emit("env-purge-doc", app.env, settings_file)


def get_settings():
    ret = []
    known_settings = sorted(guncfg.KNOWN_SETTINGS, key=lambda s: s.section)
    for i, s in enumerate(known_settings):
        if i == 0 or s.section != known_settings[i - 1].section:
            # section reference
            ret.append(".. _%s:\n\n" % (s.section.lower().replace(" ", "-").replace("_", "-")))
            # section heading
            ret.append("%s\n%s\n\n" % (s.section, "-" * len(s.section)))
        ret.append(fmt_setting(s))

    return HEAD + "".join(ret)

class SettingsRSTParser(RSTParser):
    def parse(self, inputstring, document):
        if document.current_source.endswith("/settings.rst"):
            inputstring = get_settings()
        return super().parse(inputstring, document)

def needline(line):
    # do not document decorators: just an artifact how we define our defaults
    return not line.lstrip(" ").startswith("@")

def fmt_setting(s):
    if hasattr(s, "_default_doc"):
        val = s._default_doc
    elif callable(s.default):
        val = inspect.getsource(s.default)
        val = "\n".join("    %s" % line for line in val.splitlines() if needline(line))
        val = "\n\n.. code-block:: python\n\n" + val
    elif s.default == '':
        val = "``''``"
    else:
        val = "``%r``" % s.default

    if s.cli and s.meta:
        cli = " or ".join("``%s %s``" % (arg, s.meta) for arg in s.cli)
    elif s.cli:
        cli = " or ".join("``%s``" % arg for arg in s.cli)
    else:
        cli = ""

    out = []
    out.append(".. _%s:\n" % s.name.replace("_", "-"))
    out.append("``%s``" % s.name)
    out.append("~" * (len(s.name) + 4))
    out.append("")
    if s.cli:
        out.append("**Command line:** %s" % cli)
        out.append("")
    out.append("**Default:** %s" % val)
    out.append("")
    out.append(s.desc)
    out.append("")
    out.append("")
    return "\n".join(out)


def issue_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    has_title, title, number = split_explicit_title(text)
    issue = int(utils.unescape(number))
    text = 'issue %d' % (issue, )
    refnode = nodes.reference(title, title, refuri=ISSUE_URI % issue)
    return [refnode], []


def pull_request_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    has_title, title, number = split_explicit_title(text)
    issue = int(utils.unescape(number))
    text = 'pull request %d' % (issue, )
    refnode = nodes.reference(title, title, refuri=PULL_REQUEST_URI % issue)
    return [refnode], []


def setup(app):
    app.require_sphinx((7,1))

    # strategy A: overwrite source/settings.rst
    # app.connect('builder-inited', format_settings)
    # strategy B: leave file as-is, always patch input string on parsing
    app.add_source_parser(SettingsRSTParser, True)
    # can still access reference list using:
    # python -m sphinx.ext.intersphinx _build/html/objects.inv

    app.add_role('issue', issue_role)
    app.add_role('pr', pull_request_role)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
