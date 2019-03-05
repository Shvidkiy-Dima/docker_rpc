class WebSocketRpcRoute:

    def __init__(self, method, in_thread=False):
        self.method = method
        self.in_thread = in_thread


    def _resolve(self):
        method = getattr(self, self.method, 0)
        if method:
            method.__dict__['in_thread'] = self.in_thread
        return method

    @classmethod
    def route(cls, *args, **kwargs):
        def inner():
            self = cls(*args, **kwargs)
            return self
        return inner

