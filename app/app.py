from tornado.web import Application,  StaticFileHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from settings import Settings
from api import DockerHandler

import argparse
import os



class MyApp(Application):
    def __init__(self):
        handlers = [('/ws/', DockerHandler),
                    (r'/(.*)', StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), 'static'),
                                                   'default_filename': "index.html"})]

        settings = Settings.get_settings()
        super().__init__(handlers=handlers, **settings)





if __name__ == '__main__':

    app = MyApp()
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=Settings.PORT)
    port = int(parser.parse_args().port)

    server = HTTPServer(app)
    server.listen(port)
    IOLoop.current().start()

