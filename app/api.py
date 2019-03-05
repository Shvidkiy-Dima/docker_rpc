from websocket_rpc.handler import WebSocketRpcHandler
from websocket_rpc.route import WebSocketRpcRoute
from websocket_rpc.logs import logger
from docker_utils.serializer import SerializeDocker
from info import info

from urllib.parse import urlparse
from settings import Settings

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



class DockerHandler(WebSocketRpcHandler):
    VERSION = '1.0'

    def check_origin(self, origin):
        """ check only domain without port or ORIGIN_DOMAINS from settings"""
        origin = urlparse(origin).hostname or ''
        host = self.request.headers.get("Host").split(':')[0]
        return origin == host or origin in Settings.ORIGIN_DOMAINS

########## ROUTES ##########################

"""
on_message(request)-> DockerHandler.ROUTES['method']()-> DockerHandlerInstance._resolve()-> method()-> _send(response)
"""

DockerHandler.ROUTES['info'] = DockerRoute.route(method_name='info')

DockerHandler.ROUTES['get_images'] = DockerRoute.route(method_name='get_images',  in_thread=True)
DockerHandler.ROUTES['get_containers'] = DockerRoute.route(method_name='get_containers', in_thread=True)

DockerHandler.ROUTES['run_container'] = DockerRoute.route(method_name='run_container',  in_thread=True)
DockerHandler.ROUTES['stop_container'] = DockerRoute.route(method_name='stop_container',  in_thread=True)
DockerHandler.ROUTES['start_container'] = DockerRoute.route(method_name='start_container',  in_thread=True)
DockerHandler.ROUTES['delete_container'] = DockerRoute.route(method_name='delete_container',  in_thread=True)

