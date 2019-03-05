

from tornado.options import define, options


define('test', '12')

print(options.items())





class Settings:
    TEMPLATE_PATH = 'templates'
    DATE_FORMAT = '%H:%M_%d-%m-%Y'
    ORIGIN_DOMAINS = ['localhost']

    @classmethod
    def get_settings(cls):
        return {k.lower(): v for k, v in cls.__dict__.items() if k.isupper()}






