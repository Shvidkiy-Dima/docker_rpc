
class Settings:
    PORT = 8000
    ORIGIN_DOMAINS = ['localhost']
    TEMPLATE_PATH = 'templates'

    @classmethod
    def get_settings(cls):
        return {k.lower(): v for k, v in cls.__dict__.items() if k.isupper()}






