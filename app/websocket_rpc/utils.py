from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from contextlib import contextmanager
from multiprocessing import Process

import json


@contextmanager
def error_handler(callback):
    # Call callback and put error
    try:
        yield
    except Exception as e:
        callback(e)



def from_json(data):
    return json.loads(data)



def get_params(data):
    """Expected [], {} or append object in list"""
    args, kwargs = [], {}
    if data:
        if isinstance(data, dict):
            kwargs.update(data)
        elif isinstance(data, list):
            args.extend(data)
        else:
            args.append(data)
    return args, kwargs


class ServerProcess(Process):
    def __init__(self, test_app, test_sock):
        self.test_app = test_app
        self.sock = test_sock
        super().__init__(daemon=True)

    def run(self):
        app = self.test_app()
        self.server = HTTPServer(app)
        self.server.add_socket(self.sock)
        IOLoop.current().start()

    def terminate(self):
        self.server.stop()
        self.sock.close()
        super().terminate()

