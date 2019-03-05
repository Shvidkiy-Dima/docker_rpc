from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.concurrent import Future
from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop
from tornado.locks import Lock

from functools import partial
from .utils import get_params, from_json, error_handler
from .logs import logger

import os





class WebSocketRpcHandler(WebSocketHandler):
    ROUTES = {}
    loop = IOLoop.current()
    loop.set_default_executor(ThreadPoolExecutor(max_workers=os.environ.get('MAX_THREADS')))


    def resolve_method(self, data):
        method_name = data.get('method')
        route = self.ROUTES.get(method_name)
        method = route()._resolve() if route else 0
        if not method:
            logger.error('Method %s not implemented' % method_name)
            raise NotImplementedError('Method %s not implemented: client %s' % (method_name, self))
        return method

    def method_parser(self, data):
        args, kwargs = get_params(data['params'])
        method = self.resolve_method(data)
        return method, args, kwargs


    async def open(self, *args, **kwargs):
        self.lock = Lock()
        logger.info('Client connected: %s' % self)

    def _send(self, **kwargs):
        try:
            self.write_message(kwargs)
        except WebSocketClosedError as e:
            logger.error('WebSocket closed error %s: client %s' % (self, e))
            self.close()


    def send_error(self, e):
        error = {'name': type(e).__name__, 'msg': str(e)}
        logger.error('Error %(name)s: %(msg)s' % error)
        self._send(version=self.VERSION, type='error', result=error)



    async def on_message(self, msg):
        logger.info('Client %s send message: "%s"' % (self, msg))
        with error_handler(self.send_error):
            async with self.lock:
                data = from_json(msg)
                id_ = data.get('id')
                m, a, k = self.method_parser(data)

                #expect json or json serializable object
                result = await self._thread_executor(m, *a, **k) if m.in_thread is True else await self._executor(m, *a, **k)
                self._send(result=result, id=id_, version=self.VERSION, type='success')


    async def _thread_executor(self, method, *args, **kwargs):
        loop = IOLoop.current()
        result = await loop.run_in_executor(None, partial(method, *args, **kwargs))
        return result


    async def _executor(self, method, *args, **kwargs):
        result = method(*args, **kwargs)
        if isinstance(result, Future):
            result = await result
        return result

    def __str__(self):
        return str(id(self))

    def on_close(self):
        logger.info('Client %s disconnected. Code %s Reason %s' % (self, self.close_code or '-', self.close_reason or '-'))

