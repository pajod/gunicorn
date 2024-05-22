import sys
import os
import logging

if sys.version_info >= (3, 8):
    logging.basicConfig(force=True)
    logger = logging.getLogger(__name__)
    logger.info("logger has been reset")
else:
    logging.basicConfig()
    logger = logging.getLogger(__name__)

from qdrant_client import QdrantClient
client = QdrantClient(url="https://test.cloud.qdrant.io.invalid:6333", api_key="1")

def app(environ_, start_response):
    info = "stderr from app platform=%r %r user=%r:%r:%r pid=%r" % (sys.platform, os.uname(), os.getuid(), os.getgid(), os.getgroups(), os.getpid())
    print(info, file=sys.stderr)
    # needed for Python <= 3.8
    sys.stderr.flush()
    body = b"response body from app\n%s\n" % (info.encode(), )
    response_head = [
        ("Content-Type", "text/plain; encoding=utf-8"),
        ("Content-Length", "%d" % len(body)),
    ]
    start_response("200 OK", response_head)
    return iter([body])
