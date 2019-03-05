from tornado.testing import main, gen_test, AsyncHTTPTestCase
from tornado.websocket import websocket_connect
from tornado.gen import multi

from app import MyApp

from unittest import defaultTestLoader
from uuid import uuid4
import json, docker, os


class TestWebSockets(AsyncHTTPTestCase):
    VERSION = '1.0'

    def get_app(self):
        return MyApp()

    def setUp(self):
        super().setUp()
        self.conn = self.io_loop.run_sync(lambda : websocket_connect("ws://localhost:" + str(self.get_http_port()) + "/ws/"))

    def tearDown(self):
        self.conn.close()
        super().tearDown()


    @classmethod
    def setUpClass(cls):
        cls.doc_client = docker.from_env()
        test_container = cls.doc_client.containers.run('nginx', detach=True)
        test_container.stop()
        cls.test_container_id = test_container.id
        super().setUpClass()


    async def send_msg(self, data):
        """Send msg to the server"""
        await self.conn.write_message(data)
        return await self.conn.read_message()



    def check_msg(self, msg, id,  action):
        """ Check msg version, id and type"""
        msg = json.loads(msg)
        self.assertTrue(msg.get('version') == self.VERSION)
        self.assertTrue(id == msg['id'], '%s :%s excepted - %s (%s)' % (action, msg.get('id'), id, msg.get('result') or ''))
        self.assertTrue(msg.get('type') == 'success')

    @gen_test
    def test_info(self):
        """Method 'info' """
        id = '1'
        send_data = json.dumps({'method': 'info', 'params': None, 'version': '1.0', 'id': id})
        msg = yield self.send_msg(send_data)
        self.check_msg(msg, id, 'info')

    @gen_test
    def test_run(self):
        """Method 'run' """
        id = '1'
        send_data = json.dumps({'method': 'run_container', 'params': {'id': 'nginx'} , 'version': self.VERSION, 'id': id})
        msg = yield self.send_msg(send_data)
        self.check_msg(msg, id, 'run')

    @gen_test
    def test_start(self):
        """Method 'start' """
        id = '1'
        send_data = json.dumps({'method': 'start_container', 'params': {'id': self.test_container_id} ,
                                'version': self.VERSION, 'id': id})
        msg = yield self.send_msg(send_data)
        self.check_msg(msg, id, 'start')

    @gen_test
    def test_stop(self):
        """Method 'stop' """
        id = '1'
        send_data = json.dumps({'method': 'stop_container', 'params': {'id': self.test_container_id},
                                'version': '1.0', 'id': id})
        msg = yield self.send_msg(send_data)
        self.check_msg(msg, id, 'stop')

    @gen_test
    def test_delete(self):
        """Method 'delete' """
        c = self.doc_client.containers.run('nginx', detach=True)
        c.stop()
        id = '1'
        send_data = json.dumps({'method': 'delete_container', 'params': {'id': c.id}, 'version': '1.0', 'id': id})
        msg = yield self.send_msg(send_data)
        self.check_msg(msg, id, 'delete')

    @gen_test
    def test_get_images(self):
        """Method 'get_images' """
        id = '1'
        send_data = json.dumps({'method': 'get_images', 'params': None, 'version': '1.0', 'id': id})
        msg = yield self.send_msg(send_data)
        self.check_msg(msg, id, 'get_images')

    @gen_test
    def test_get_containers(self):
        """Method 'get_containers' """
        id = '1'
        send_data = json.dumps({'method': 'get_containers', 'params': {'status': 'running'}, 'version': '1.0', 'id': id})
        msg = yield self.send_msg(send_data)
        self.check_msg(msg, id, 'get_containers')

    @gen_test
    def test_method_not_implemented(self):
        """When server received not implemented method"""
        method = str(uuid4())
        send_data = json.dumps({'method': method, 'params': None, 'version': '1.0', 'id': '1'})
        msg = yield self.send_msg(send_data)
        msg = json.loads(msg)
        self.assertTrue(msg['type'] == 'error')
        self.assertTrue(msg['result']['name'] == 'NotImplementedError' or msg['result']['name'] == 'NotImplemented')



    async def check_con_msg(self, data, id):
        data['id'] = str(id)
        msg = await self.send_msg(json.dumps(data))
        self.check_msg(msg, str(id), '')


    @gen_test()
    def test_connection(self):
        """ Many msgs from one client """
        count = int(os.environ.get('COUNT_CONNECTION') or 40)
        start = {'method': 'start_container', 'params': {'id': self.test_container_id} ,'version': self.VERSION}
        stop = {'method': 'stop_container', 'params': {'id': self.test_container_id}, 'version': self.VERSION}
        yield multi([self.check_con_msg(stop, id) for id in range(count // 2)] + \
                         [self.check_con_msg(start, id) for id in range(count // 2)])





def all():
    return defaultTestLoader.loadTestsFromTestCase(TestWebSockets)

if __name__ == '__main__':
    main()

