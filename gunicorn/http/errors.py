# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

# We don't need to call super() in __init__ methods of our
# BaseException and Exception classes because we also define
# our own __str__ methods so there is no need to pass 'message'
# to the base class to get a meaningful output from 'str(exc)'.
# pylint: disable=super-init-not-called


class ParseException(Exception):
    code = 400
    reason = "Bad Request"


class NoMoreData(IOError):
    def __init__(self, buf=None):
        self.buf = buf

    def __str__(self):
        return "No more data after: %r" % (self.buf, )


class ConfigurationProblem(Exception):
    code = 500
    reason = "Internal Server Error"

    def __init__(self, info):
        self.info = info

    def __str__(self):
        return "Configuration problem: %s" % (self.info, )


class ExpectationFailed(ParseException):
    reason = "Expectation Failed"
    code = 417

    def __init__(self, expect):
        self.expect = expect

    def __str__(self):
        return "Expectation failed: %r" % (self.expect, )


class InvalidRequestLine(ParseException):
    code = 400
    # note: rfc9112 section 3 permits 501 for long method, 414 for long URI

    def __init__(self, req):
        self.req = req

    def __str__(self):
        return "Invalid HTTP request line: %r" % (self.req, )


class InvalidRequestMethod(ParseException):
    # not to be confused with: 405 Method Not Allowed

    def __init__(self, method):
        self.method = method

    def __str__(self):
        return "Invalid HTTP method: %r" % (self.method, )


class InvalidHTTPVersion(ParseException):
    def __init__(self, version):
        self.version = version

    def __str__(self):
        return "Invalid HTTP Version: %r" % (self.version, )


class InvalidHeader(ParseException):
    def __init__(self, hdr, req=None):
        self.hdr = hdr
        self.req = req

    def __str__(self):
        return "Invalid HTTP Header: %r" % (self.hdr, )


class IncompleteBody(ParseException):
    def __str__(self):
        return "Incomplete Request Body"


class ObsoleteFolding(ParseException):
    def __init__(self, hdr):
        self.hdr = hdr

    def __str__(self):
        return "Obsolete line folding is unacceptable: %r" % (self.hdr, )


class InvalidHeaderName(ParseException):
    def __init__(self, hdr):
        self.hdr = hdr

    def __str__(self):
        return "Invalid HTTP header name: %r" % (self.hdr, )


class UnsupportedTransferCoding(ParseException):
    code = 501

    def __init__(self, hdr):
        self.hdr = hdr

    def __str__(self):
        return "Unsupported transfer coding: %r" % (self.hdr, )


class InvalidChunkSize(IOError):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "Invalid chunk size: %r" % (self.data, )


class ChunkMissingTerminator(IOError):
    def __init__(self, term):
        self.term = term

    def __str__(self):
        return "Invalid chunk terminator is not '\\r\\n': %r" % (self.term, )


class LimitRequestLine(ParseException):
    def __init__(self, size, max_size):
        self.size = size
        self.max_size = max_size

    def __str__(self):
        return "Request Line is too large (%s > %s)" % (self.size, self.max_size)


class LimitRequestHeaders(ParseException):
    code = 431
    reason = "Request Header Fields Too Large"

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        # FIXME: verbose. maybe just return reason?
        return "Error parsing headers: '%s'" % (self.reason, )


class InvalidProxyLine(ParseException):
    code = 400

    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "Invalid PROXY line: %r" % (self.line, )


class ForbiddenProxyRequest(ParseException):
    reason = "Forbidden"
    code = 403

    def __init__(self, host):
        self.host = host

    def __str__(self):
        return "Proxy request from %r not allowed" % (self.host, )


class InvalidSchemeHeaders(ParseException):
    def __str__(self):
        return "Contradictory scheme headers"
