import importlib
import os
import secrets
import signal
import subprocess
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import NamedTuple, Self, Any
    import http.client

import pytest

# pytest does not like exceptions from threads
#  - so use subprocess.Popen for now
# from threading import Thread, Event


GRACEFUL_TIMEOUT = 10
BOOT_DEADLINE = 40

# test flaky for WORKER_COUNT != 1, awaiting *last* worker not implemented
WORKER_COUNT = 1
APP_BASENAME = "testsyntax"
APP_APPNAME = "myapp"

TEST_SIMPLE = [
    pytest.param("sync"),
    "eventlet",
    "gevent",
    "gevent_wsgi",
    "gevent_pywsgi",
    "tornado",
    "gthread",
    "aiohttp.GunicornWebWorker",
    "aiohttp.GunicornUVLoopWebWorker",
]  # type: list[str|NamedTuple]

TEST_TOLERATES_MAX_REQUESTS = [
    pytest.param("sync"),
    # pytest.param("expected_failure", marks=pytest.mark.xfail),
    "eventlet",
    "gevent",
    "gevent_wsgi",
    "gevent_pywsgi",
    "tornado",
    "gthread",
    # "aiohttp.GunicornWebWorker",
    # "aiohttp.GunicornUVLoopWebWorker",
]  # type: list[str|NamedTuple]

TEST_TOLERATES_BAD_BOOT = [
    pytest.param("sync"),
    # pytest.param("expected_failure", marks=pytest.mark.xfail),
    "eventlet",
    "gevent",
    "gevent_wsgi",
    "gevent_pywsgi",
    "tornado",
    "gthread",
    # "aiohttp.GunicornWebWorker",
    # "aiohttp.GunicornUVLoopWebWorker",
]  # type: list[str|NamedTuple]

TEST_TOLERATES_BAD_RELOAD = [
    pytest.param("sync"),
    # pytest.param("expected_failure", marks=pytest.mark.xfail),
    "eventlet",
    "gevent",
    "gevent_wsgi",
    "gevent_pywsgi",
    "tornado",
    "gthread",
    # "aiohttp.GunicornWebWorker",
    # "aiohttp.GunicornUVLoopWebWorker",
]  # type: list[str|NamedTuple]

WORKER_DEPENDS = {
    "aiohttp.GunicornWebWorker": ["aiohttp"],
    "aiohttp.GunicornUVLoopWebWorker": ["aiohttp", "uvloop"],
    "uvicorn.workers.UvicornWorker": ["uvicorn"],  # deprecated
    "uvicorn.workers.UvicornH11Worker": ["uvicorn"],  # deprecated
    "uvicorn_worker.UvicornWorker": ["uvicorn_worker"],
    "uvicorn_worker.UvicornH11Worker": ["uvicorn_worker"],
    "eventlet": ["eventlet"],
    "gevent": ["gevent"],
    "gevent_wsgi": ["gevent"],
    "gevent_pywsgi": ["gevent"],
    "tornado": ["tornado"],
}
DEP_WANTED = set(sum(WORKER_DEPENDS.values(), start=[]))  # type: set[str]
DEP_INSTALLED = set()  # type: set[str]

for dependency in DEP_WANTED:
    try:
        importlib.import_module(dependency)
        DEP_INSTALLED.add(dependency)
    except ImportError:
        pass

for worker_name, worker_needs in WORKER_DEPENDS.items():
    missing = list(pkg for pkg in worker_needs if pkg not in DEP_INSTALLED)
    if missing:
        for T in (
            TEST_TOLERATES_BAD_BOOT,
            TEST_TOLERATES_BAD_RELOAD,
            TEST_TOLERATES_MAX_REQUESTS,
            TEST_SIMPLE,
        ):
            if worker_name not in T:
                continue
            T.remove(worker_name)
            skipped_worker = pytest.param(
                worker_name, marks=pytest.mark.skip("%s not installed" % (missing[0]))
            )
            T.append(skipped_worker)

PY_OK = """
import sys
import logging

if sys.version_info >= (3, 8):
    logging.basicConfig(force=True)
    logger = logging.getLogger(__name__)
    logger.info("logger has been reset")
else:
    logging.basicConfig()
    logger = logging.getLogger(__name__)

import syntax_ok

def myapp(environ, start_response):
    # print("stdout from app", file=sys.stdout)
    print("stderr from app: C-L=%s" % (environ.get("CONTENT_LENGTH", "-")), file=sys.stderr)
    # needed for Python <= 3.8
    sys.stderr.flush()
    body = b"response body from app"
    response_head = [
        ("Content-Type", "text/plain"),
        ("Content-Length", "%d" % len(body)),
    ]
    start_response("200 OK", response_head)
    return iter([body])
"""

PY_OK_AIOHTTP = """
import sys
import logging

if sys.version_info >= (3, 8):
    logging.basicConfig(force=True)
    logger = logging.getLogger(__name__)
    logger.info("logger has been reset")
else:
    logging.basicConfig()
    logger = logging.getLogger(__name__)

import syntax_ok

from aiohttp import web

async def index(req_):
    print("stderr from app", file=sys.stderr)
    # needed for Python <= 3.8
    sys.stderr.flush()
    return web.Response(text="response body from app")

myapp = web.Application()
myapp.router.add_get("/", index)
"""

PY_VALID_CONFIG = """
def post_fork(a_, b_): pass
def post_worker_init(_): pass
"""

PY_GOOD_IMPORT = """
def good_method():
    pass
"""

# some interesting alternatives to SyntaxError:
# * os.kill(os.getppid(), signal.SIGTERM)
# * sys.exit(3)
# * raise KeyboardInterrupt
PY_BAD_IMPORT = """
def bad_method():
    syntax_error:
"""

PY_BAD = """
import sys
import logging

if sys.version_info >= (3, 8):
    logging.basicConfig(force=True)
    logger = logging.getLogger(__name__)
    logger.info("logger has been reset")
else:
    logger = logging.getLogger(__name__)
    logging.basicConfig()

import syntax_ok
import syntax_error

def myapp(environ_, start_response_):
    raise RuntimeError("The SyntaxError should raise")
"""

PY_BAD_AIOHTTP = """
import sys
import logging

if sys.version_info >= (3, 8):
    logging.basicConfig(force=True)
    logger = logging.getLogger(__name__)
    logger.info("logger has been reset")
else:
    logger = logging.getLogger(__name__)
    logging.basicConfig()

import syntax_ok
import syntax_error

from aiohttp import web

async def index(req_):
    raise RuntimeError("The SyntaxError should raise")
myapp = web.Application()
myapp.router.add_get("/", index)
"""


class Server:
    def __init__(
        self,
        *,
        temp_path,
        server_bind,
        worker_class,
        start_valid=True,
        use_config=False,
        public_traceback=True,
    ):
        # type: (Path, str, str, bool, bool, bool) -> None
        # super().__init__(*args, **kwargs)
        # self.launched = Event()
        self.p = None  # type: subprocess.Popen[bytes] | None
        assert isinstance(temp_path, Path)
        self.temp_path = temp_path
        self.py_path = (temp_path / ("%s.py" % APP_BASENAME)).absolute()
        self.conf_path = (
            (temp_path / "gunicorn.conf.py").absolute()
            if use_config
            else Path(os.devnull)
        )
        self._PY_OK = PY_OK
        self._PY_BAD = PY_BAD
        if worker_class.startswith("aiohttp"):
            self._PY_OK = PY_OK_AIOHTTP
            self._PY_BAD = PY_BAD_AIOHTTP
        self._write_initial = self.write_ok if start_valid else self.write_bad
        self._argv = [
            sys.executable,
            "-m",
            "gunicorn",
            "--config=%s" % self.conf_path,
            "--log-level=debug",
            "--worker-class=%s" % worker_class,
            "--workers=%d" % WORKER_COUNT,
            "--buf-read-size=77",
            "--enable-stdio-inheritance",
            "--access-logfile=-",
            "--disable-redirect-access-to-syslog",
            "--graceful-timeout=%d" % (GRACEFUL_TIMEOUT,),
            "--if-no-app={}".format("world-readable" if public_traceback else "quiet"),
            # "--reload",
            # sandwich the one we care for: verify multiple instances of --reload-extra
            "--reload-extra",
            "{}".format(self.temp_path / "syntax_ok.py"),
            f"{self.py_path}",
            "{}".format(self.temp_path / "syntax_ok.py"),
            # FIXME: not utilizing inotify reduces test coverage
            "--reload-engine=poll",
            "--bind=%s" % server_bind,
            "--reuse-port",
            "--",
            f"{APP_BASENAME}:{APP_APPNAME}",
        ]

    def write_bad(self):
        # type: () -> None
        with open(self.py_path, "w+") as f:
            f.write(self._PY_BAD)

    def write_ok(self):
        # type: () -> None
        with open(self.py_path, "w+") as f:
            f.write(self._PY_OK)

    def _write_support(self):
        # type: () -> None
        with open(self.conf_path, "w+") as f:
            f.write(PY_VALID_CONFIG)
        with open(self.temp_path / "syntax_error.py", "w+") as f:
            f.write(PY_BAD_IMPORT)
        with open(self.temp_path / "syntax_ok.py", "w+") as f:
            f.write(PY_GOOD_IMPORT)

    def __enter__(self):
        # type: () -> Self
        self._write_support()
        self._write_initial()
        self.run()
        return self

    def __exit__(self, *exc):
        # type: (*Any) -> None
        if self.p is None:
            return
        self.p.send_signal(signal.SIGKILL)
        stdout, stderr = self.p.communicate(timeout=2 + GRACEFUL_TIMEOUT)
        ret = self.p.returncode
        assert stdout == b"", stdout
        assert ret == 0, (ret, stdout, stderr)

    def run(self):
        # type: () -> None
        self.p = subprocess.Popen(
            self._argv,
            bufsize=0,  # allow read to return short
            cwd=self.temp_path,
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
        assert self.p.stdout is not None  # this helps static type checkers
        assert self.p.stderr is not None  # this helps static type checkers
        os.set_blocking(self.p.stdout.fileno(), False)
        os.set_blocking(self.p.stderr.fileno(), False)
        # self.launched.set()

    def graceful_quit(self, expect=None):
        # type: (set[str]|None) -> str
        if self.p is None:
            raise RuntimeError("called graceful_quit() when not running")
        self.p.send_signal(signal.SIGTERM)
        # self.p.kill()
        stdout, stderr = self.p.communicate(timeout=2 + GRACEFUL_TIMEOUT)
        assert stdout == b""
        exitcode = self.p.poll()  # will return None if running
        assert exitcode == 0, (exitcode, stdout, stderr)
        self.p = None
        ret = stderr.decode("utf-8", "surrogateescape")
        for keyword in expect or ():
            assert keyword in ret, (keyword, ret)
        return ret

    def read_stdio(self, *, key, timeout_sec, wait_for_keyword, expect=None):
        # type: (int, int, str, set[str]|None) -> str
        # try:
        #    stdout, stderr = self.p.communicate(timeout=timeout)
        # except subprocess.TimeoutExpired:
        buf = ["", ""]
        seen_keyword = 0
        unseen_keywords = list(expect or [])
        poll_per_second = 30
        assert self.p is not None  # this helps static type checkers
        assert self.p.stdout is not None  # this helps static type checkers
        assert self.p.stderr is not None  # this helps static type checkers
        for _ in range(timeout_sec * poll_per_second):
            for fd, file in enumerate([self.p.stdout, self.p.stderr]):
                read = file.read(64 * 1024)
                if read is not None:
                    buf[fd] += read.decode("utf-8", "surrogateescape")
            if seen_keyword or wait_for_keyword in buf[key]:
                seen_keyword += 1
            for additional_keyword in tuple(unseen_keywords):
                for somewhere in buf:
                    if additional_keyword in somewhere:
                        unseen_keywords.remove(additional_keyword)
            # gathered all the context we wanted
            if seen_keyword and not unseen_keywords:
                break
            # not seen expected output? wait for % of original timeout
            # .. maybe we will still see better error context that way
            if seen_keyword > (0.75 * timeout_sec * poll_per_second):
                break
            time.sleep(1.0 / poll_per_second)
        # assert buf[abs(key - 1)] == ""
        assert wait_for_keyword in buf[key], (wait_for_keyword, *buf)
        assert not unseen_keywords, (unseen_keywords, *buf)
        return buf[key]


class Client:
    def __init__(self, host_port):
        # type: (str) -> None
        self._host_port = host_port

    def truncated(self):
        # type: () -> http.client.HTTPResponse
        import http.client

        conn = http.client.HTTPConnection(self._host_port, timeout=2)
        declared_cl = 30
        body = "shorter than %d bytes" % (declared_cl,)
        assert len(body) < declared_cl
        conn.request(
            "GET",
            "/",
            headers={"Host": "localhost", "Content-Length": "%d" % (declared_cl,)},
            body=body,
        )
        return conn.getresponse()

    def valid(self):
        # type: () -> http.client.HTTPResponse
        import http.client

        conn = http.client.HTTPConnection(self._host_port, timeout=2)
        conn.request("GET", "/", headers={"Host": "localhost"}, body="GETBODY!")
        return conn.getresponse()


@pytest.mark.parametrize("worker_class", TEST_SIMPLE)
def test_process_request_after_invalid_request(worker_class):
    # type: (str) -> None

    # 1. start up the server with valid app
    # 2. send some malformed requests
    # 3. send some valid requests - server should still respond OK

    fixed_port = 1024 * 6 + secrets.randbelow(1024 * 9)
    # FIXME: should also test inherited socket (LISTEN_FDS)
    server_bind = "[::1]:%d" % fixed_port

    client = Client(server_bind)

    with TemporaryDirectory(suffix="_temp_py") as tempdir_name:
        with Server(
            server_bind=server_bind,
            worker_class=worker_class,
            temp_path=Path(tempdir_name),
            start_valid=True,
        ) as server:
            OUT = 0
            ERR = 1

            _boot_log = server.read_stdio(
                key=ERR,
                wait_for_keyword="Arbiter booted",
                timeout_sec=BOOT_DEADLINE,
                expect={
                    "Booting worker",
                },
            )

            # worker did boot now, request should be replied but not succeed
            response = client.truncated()
            assert response.status == 400, (response.status, response.reason)
            assert response.reason == "OK", response.reason
            assert response.reason == "Invalid Request", response.reason
            body = response.read(64 * 1024).decode("utf-8", "surrogateescape")

            _access_log = server.read_stdio(
                key=OUT,
                wait_for_keyword='"GET / HTTP/1.1" 400 ',
                timeout_sec=BOOT_DEADLINE,
            )

            # worker still responsive, this request should work
            response = client.valid()
            assert response.status == 200, (response.status, response.reason)
            assert response.reason == "OK", response.reason
            body = response.read(64 * 1024).decode("utf-8", "surrogateescape")
            assert "response body from app" == body, (body,)

            _access_log = server.read_stdio(
                key=OUT,
                wait_for_keyword='"GET / HTTP/1.1" 200 ',
                timeout_sec=BOOT_DEADLINE,
            )

            _shutdown_log = server.graceful_quit(
                expect={
                    "Handling signal: term",
                    # FIXME: broken on PyPy + gevent, skip asserting this line for now
                    # "Worker exiting ",
                    "Shutting down: Master",
                },
            )


@pytest.mark.parametrize("worker_class", TEST_TOLERATES_BAD_BOOT)
def test_process_request_after_fixing_syntax_error(worker_class):
    # type: (str) -> None

    # 1. start up the server with invalid app
    # 2. fixup the app by writing to file
    # 3. await reload: the app should begin working soon

    fixed_port = 1024 * 6 + secrets.randbelow(1024 * 9)
    # FIXME: should also test inherited socket (LISTEN_FDS)
    server_bind = "[::1]:%d" % fixed_port

    client = Client(server_bind)

    with TemporaryDirectory(suffix="_temp_py") as tempdir_name:
        with Server(
            worker_class=worker_class,
            server_bind=server_bind,
            temp_path=Path(tempdir_name),
            start_valid=False,
            public_traceback=False,
        ) as server:
            OUT = 0
            ERR = 1

            _boot_log = server.read_stdio(
                key=ERR,
                wait_for_keyword="Arbiter booted",
                timeout_sec=BOOT_DEADLINE,
                expect={
                    "SyntaxError: invalid syntax",
                    f'{APP_BASENAME}.py", line ',
                },
            )

            # raise RuntimeError(boot_log)

            # worker could not load, request will fail
            response = client.valid()
            assert response.status == 500, (response.status, response.reason)
            assert response.reason == "Internal Server Error", response.reason
            body = response.read(64 * 1024).decode("utf-8", "surrogateescape")
            # --if-no-app=quiet responds, but does NOT share traceback
            assert "error" in body.lower()
            assert "load_wsgi" not in body.lower()

            _access_log = server.read_stdio(
                key=OUT,
                wait_for_keyword='"GET / HTTP/1.1" 500 ',
                timeout_sec=BOOT_DEADLINE,
            )
            # trigger reloader
            server.write_ok()
            # os.utime(editable_file)

            _reload_log = server.read_stdio(
                key=ERR,
                wait_for_keyword="reloading",
                timeout_sec=BOOT_DEADLINE,
                expect={
                    f"{APP_BASENAME}.py modified",
                    "Booting worker",
                },
            )

            # worker did boot now, request should work
            response = client.valid()
            assert response.status == 200, (response.status, response.reason)
            assert response.reason == "OK", response.reason
            body = response.read(64 * 1024).decode("utf-8", "surrogateescape")
            assert "response body from app" == body, (body,)

            _debug_log = server.read_stdio(
                key=ERR,
                wait_for_keyword="stderr from app",
                timeout_sec=BOOT_DEADLINE,
                expect={
                    # read access log
                    '"GET / HTTP/1.1"',
                },
            )

            _shutdown_log = server.graceful_quit(
                expect={
                    "Handling signal: term",
                    # FIXME: broken on PyPy + gevent, skip asserting this line for now
                    # "Worker exiting ",
                    "Shutting down: Master",
                }
            )


@pytest.mark.parametrize("worker_class", TEST_TOLERATES_BAD_RELOAD)
def test_process_shutdown_cleanly_after_inserting_syntax_error(worker_class):
    # type: (str) -> None

    # 1. start with valid application
    # 2. now insert fatal error by writing to app
    # 3. await reload, the shutdown gracefully

    fixed_port = 1024 * 6 + secrets.randbelow(1024 * 9)
    # FIXME: should also test inherited socket (LISTEN_FDS)
    server_bind = "[::1]:%d" % fixed_port

    client = Client(server_bind)

    with TemporaryDirectory(suffix="_temp_py") as tempdir_name:
        with Server(
            server_bind=server_bind,
            worker_class=worker_class,
            temp_path=Path(tempdir_name),
            start_valid=True,
        ) as server:
            OUT = 0
            ERR = 1

            _boot_log = server.read_stdio(
                key=ERR,
                wait_for_keyword="Arbiter booted",
                timeout_sec=BOOT_DEADLINE,
                expect={
                    "Booting worker",
                },
            )

            # worker did boot now, request should work
            response = client.valid()
            assert response.status == 200, (response.status, response.reason)
            assert response.reason == "OK", response.reason
            body = response.read(64 * 1024).decode("utf-8", "surrogateescape")
            assert "response body from app" == body, (body,)

            _debug_log = server.read_stdio(
                key=ERR,
                wait_for_keyword="stderr from app",
                timeout_sec=BOOT_DEADLINE,
            )

            # trigger reloader
            server.write_bad()
            # os.utime(editable_file)

            # this test can fail flaky, when the keyword is not last line logged
            # .. but the worker count is only logged when changed
            _reload_log = server.read_stdio(
                key=ERR,
                wait_for_keyword="SyntaxError: ",
                # wait_for_keyword="%d workers" % WORKER_COUNT,
                timeout_sec=BOOT_DEADLINE,
                expect={
                    "reloading",
                    f"{APP_BASENAME}.py modified",
                    "SyntaxError: invalid syntax",
                    f'{APP_BASENAME}.py", line ',
                },
            )

            # worker could not load, request will fail
            response = client.valid()
            assert response.status == 500, (response.status, response.reason)
            assert response.reason == "Internal Server Error", response.reason
            body = response.read(64 * 1024).decode("utf-8", "surrogateescape")
            # its a traceback
            assert "load_wsgi" in body.lower()

            _access_log = server.read_stdio(
                key=OUT,
                wait_for_keyword='"GET / HTTP/1.1" 500 ',
                timeout_sec=BOOT_DEADLINE,
            )

            _shutdown_log = server.graceful_quit(
                expect={
                    "Handling signal: term",
                    # FIXME: broken on PyPy + gevent, skip asserting this line for now
                    # "Worker exiting ",
                    "Shutting down: Master",
                },
            )
