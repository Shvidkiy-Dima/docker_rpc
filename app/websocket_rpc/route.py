
class WebSocketRpcRoute:

    def __init__(self, method_name, in_thread=False):
        """ Executable func name  and options """
        self.method_name = method_name
        self.in_thread = in_thread


    def _resolve(self):
        """ Get method from subclass if method exists and don't magic or special """
        method = getattr(self, self.method_name, 0) if not self.method_name.startswith('_') else 0
        if method:
            # Execute in ThreadPool?
            method.__dict__['in_thread'] = self.in_thread
        return method

    @classmethod
    def route(cls, *args, **kwargs):
        """ Stateless, new msg - new instance.
        Return callable object which create new route object  """
        def route_inner():
            self = cls(*args, **kwargs)
            return self
        return route_inner

