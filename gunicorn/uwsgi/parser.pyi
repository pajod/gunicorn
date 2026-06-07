from gunicorn._protocol import ParserProtocol
from gunicorn.http.parser import Parser as Parser
from gunicorn.uwsgi.message import UWSGIRequest as UWSGIRequest

class UWSGIParser(Parser):
    mesg_class: type[ParserProtocol]
