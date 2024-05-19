# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

try:
    import importlib.metadata as importlib_metadata
except (ModuleNotFoundError, ImportError):
    import importlib_metadata

import os
import sys
import time

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

meta = importlib_metadata.metadata("gunicorn")
version = meta["Version"]
release = meta["Version"]
project = meta["Name"]
copyright = '2009-%s, Benoit Chesneau' % time.strftime('%Y')

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

DOCS_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(DOCS_DIR, os.pardir))
sys.path.insert(0, os.path.join(DOCS_DIR, os.pardir, os.pardir))

extensions = [
    'gunicorn_ext',
]

templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'Gunicorndoc'
