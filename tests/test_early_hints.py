# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

"""Tests for HTTP 103 Early Hints support (RFC 8297)."""

import pytest
from unittest import mock
from io import BytesIO

from gunicorn.http import wsgi
from gunicorn.http.errors import InvalidHeader, InvalidHeaderName


class MockConfig:
    """Mock gunicorn configuration."""

    def __init__(self):
        self.is_ssl = False
        self.workers = 1
        self.limit_request_fields = 100
        self.limit_request_field_size = 8190
        self.limit_request_line = 8190
        self.secure_scheme_headers = {}
        self.forwarded_allow_ips = ['127.0.0.1']
        self.forwarder_headers = []
        self.strip_header_spaces = False
        self.permit_obsolete_folding = False
        self.header_map = "refuse"
        self.sendfile = True
        self.errorlog = "-"

    def forwarded_allow_networks(self):
        return []


class MockRequest:
    """Mock HTTP request for testing."""

    def __init__(self, version=(1, 1)):
        self.version = version
        self.method = "GET"
        self.uri = "/"
        self.path = "/"
        self.query = ""
        self.fragment = ""
        self.scheme = "http"
        self.headers = []
        self.body = BytesIO(b"")
        self.proxy_protocol_info = None
        self._expected_100_continue = False

    def should_close(self):
        return False


class MockSocket:
    """Mock socket for testing."""

    def __init__(self):
        self._sent = bytearray()
        self._closed = False

    def sendall(self, data):
        if self._closed:
            raise OSError("Socket is closed")
        self._sent.extend(data)

    def send(self, data):
        if self._closed:
            raise OSError("Socket is closed")
        self._sent.extend(data)
        return len(data)

    def get_sent_data(self):
        return bytes(self._sent)

    def clear(self):
        self._sent = bytearray()

    def close(self):
        self._closed = True


class TestWSGIEarlyHints:
    """Test WSGI wsgi.early_hints callback."""

    def test_early_hints_callback_in_environ(self):
        """Verify wsgi.early_hints is added to environ."""
        cfg = MockConfig()
        req = MockRequest()
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        assert 'wsgi.early_hints' in environ
        assert callable(environ['wsgi.early_hints'])

    def test_send_single_early_hint(self):
        """Test sending one Link header as early hint."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 1))
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        # Send early hints
        environ['wsgi.early_hints']([
            ('Link', '</style.css>; rel=preload; as=style'),
        ])

        sent_data = sock.get_sent_data()
        assert b"HTTP/1.1 103 Early Hints\r\n" in sent_data
        assert b"Link: </style.css>; rel=preload; as=style\r\n" in sent_data
        assert sent_data.endswith(b"\r\n\r\n")

    def test_send_multiple_early_hints(self):
        """Test sending multiple Link headers."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 1))
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        environ['wsgi.early_hints']([
            ('Link', '</style.css>; rel=preload; as=style'),
            ('Link', '</app.js>; rel=preload; as=script'),
        ])

        sent_data = sock.get_sent_data()
        assert b"HTTP/1.1 103 Early Hints\r\n" in sent_data
        assert b"Link: </style.css>; rel=preload; as=style\r\n" in sent_data
        assert b"Link: </app.js>; rel=preload; as=script\r\n" in sent_data

    def test_early_hints_not_sent_for_http10(self):
        """Test that early hints are not sent for HTTP/1.0 clients."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 0))  # HTTP/1.0
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        # Try to send early hints
        environ['wsgi.early_hints']([
            ('Link', '</style.css>; rel=preload; as=style'),
        ])

        # Nothing should be sent for HTTP/1.0
        sent_data = sock.get_sent_data()
        assert sent_data == b""

    def test_multiple_early_hints_calls(self):
        """Test multiple calls to wsgi.early_hints (multiple 103 responses)."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 1))
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        # First early hints call
        environ['wsgi.early_hints']([
            ('Link', '</critical.css>; rel=preload; as=style'),
        ])

        # Second early hints call
        environ['wsgi.early_hints']([
            ('Link', '</app.js>; rel=preload; as=script'),
        ])

        sent_data = sock.get_sent_data()
        # Should have two separate 103 responses
        assert sent_data.count(b"HTTP/1.1 103 Early Hints\r\n") == 2

    def test_early_hints_with_bytes_headers(self):
        """Test early hints with bytes header values."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 1))
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        # Send with bytes values
        environ['wsgi.early_hints']([
            (b'Link', b'</style.css>; rel=preload; as=style'),
        ])

        sent_data = sock.get_sent_data()
        assert b"HTTP/1.1 103 Early Hints\r\n" in sent_data
        assert b"Link: </style.css>; rel=preload; as=style\r\n" in sent_data

    def test_empty_early_hints(self):
        """Test early hints with empty headers list."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 1))
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        # Send empty headers
        environ['wsgi.early_hints']([])

        sent_data = sock.get_sent_data()
        # Should still send 103 response with no headers
        assert sent_data == b"HTTP/1.1 103 Early Hints\r\n\r\n"

    def test_early_hints_rejects_crlf_in_header_value(self):
        """Test that CRLF in header values is rejected (response splitting)."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 1))
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        # Attempt CRLF injection in header value
        with pytest.raises(InvalidHeader):
            environ['wsgi.early_hints']([
                ('Link', '</evil>; rel=preload\r\nX-Injected: true'),
            ])

        # Nothing should have been sent
        assert sock.get_sent_data() == b""

    def test_early_hints_rejects_crlf_in_header_name(self):
        """Test that CRLF in header names is rejected."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 1))
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        with pytest.raises(InvalidHeaderName):
            environ['wsgi.early_hints']([
                ('Link\r\nX-Injected', '</evil>'),
            ])

        assert sock.get_sent_data() == b""

    def test_early_hints_rejects_invalid_header_name(self):
        """Test that invalid token characters in header name are rejected."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 1))
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        # Space is not allowed in header names
        with pytest.raises(InvalidHeaderName):
            environ['wsgi.early_hints']([
                ('Invalid Header', '</style.css>'),
            ])

    def test_early_hints_valid_headers_pass_validation(self):
        """Test that valid headers still work after adding validation."""
        cfg = MockConfig()
        req = MockRequest(version=(1, 1))
        sock = MockSocket()

        resp, environ = wsgi.create(req, sock, ('127.0.0.1', 12345),
                                    ('127.0.0.1', 8000), cfg)

        # These should all pass validation
        environ['wsgi.early_hints']([
            ('Link', '</style.css>; rel=preload; as=style'),
            ('Link', '</app.js>; rel=preload; as=script'),
            ('X-Custom-Header', 'some-value'),
        ])

        sent_data = sock.get_sent_data()
        assert b"HTTP/1.1 103 Early Hints\r\n" in sent_data
        assert b"Link: </style.css>; rel=preload; as=style\r\n" in sent_data

