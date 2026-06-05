#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

"""Pytest configuration for gunicorn tests."""

import os
import sys

import pytest

# Add the tests directory to sys.path so test support modules can be imported
# as 'tests.module_name' (e.g., 'tests.support_dirty_apps:CounterApp')
tests_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if tests_dir not in sys.path:
    sys.path.insert(0, tests_dir)


@pytest.fixture(params=["python", ])
def http_parser(request):
    """Parametrize tests over http_parser implementations."""
    if request.param == "fast":
        pytest.skip("gunicorn_h1c support removed from this unmaintained fork")
    return request.param
