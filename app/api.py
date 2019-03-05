from websocket_rpc.handler import WebSocketRpcHandler
from websocket_rpc.route import WebSocketRpcRoute
from websocket_rpc.logs import logger
from docker_utils.serializer import SerializeDocker
from info import info

from urllib.parse import urlparse

class DockerRoute(WebSocketRpcRoute):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer = SerializeDocker()

    def info(self):
        return info

    def get_images(self, **kwargs):
        data = self.serializer.get_images(**kwargs)
        return data

    def get_containers(self, **kwargs):
        data = self.serializer.get_containers(**kwargs)
        return data

    def start_container(self, id):
        self.serializer.start(id)
        logger.info('\nContainer %s was started!\n' % id)

    def run_container(self, id):
        container_data = self.serializer.run(id)
        logger.info('\nContainer %s was ran!\n' % id)
        return container_data

    def stop_container(self, id):
        self.serializer.stop(id)
        logger.info('\nContainer %s was stopped!\n' % id)

    def delete_container(self, id):
        self.serializer.delete(id)
        logger.info('\nContainer %s was deleted!\n' % id)


from tornado.options import options
class DockerHandler(WebSocketRpcHandler):
    VERSION = '1.0'

    def check_origin(self, origin):
        origin = urlparse(origin).hostname or ''
        host = urlparse(self.request.headers.get("Host")).hostname
        print(origin, host, options.items(), '---------------------------------')
        return True
        # return origin == host and origin in

DockerHandler.ROUTES['info'] = DockerRoute.route(method='info')

DockerHandler.ROUTES['get_images'] = DockerRoute.route(method='get_images',  in_thread=True)
DockerHandler.ROUTES['get_containers'] = DockerRoute.route(method='get_containers', in_thread=True)

DockerHandler.ROUTES['run_container'] = DockerRoute.route(method='run_container',  in_thread=True)
DockerHandler.ROUTES['stop_container'] = DockerRoute.route(method='stop_container',  in_thread=True)
DockerHandler.ROUTES['start_container'] = DockerRoute.route(method='start_container',  in_thread=True)
DockerHandler.ROUTES['delete_container'] = DockerRoute.route(method='delete_container',  in_thread=True)

