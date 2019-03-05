from tornado.web import Application, RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


from api import DockerHandler
from settings import Settings

import argparse


class Index(RequestHandler):

    def get(self):
        self.render('index.html')

class MyApp(Application):
    def __init__(self):
        handlers = [('/', Index),
                    ('/ws/', DockerHandler)]

        settings = Settings.get_settings()
        super().__init__(handlers=handlers, **settings)





if __name__ == '__main__':

    app = MyApp()
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=8000)
    port = int(parser.parse_args().port)

    server = HTTPServer(app)
    server.listen(port)
    IOLoop.current().start()

