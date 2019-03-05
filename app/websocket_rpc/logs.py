import logging
from logging import StreamHandler


logger = logging.getLogger('main')
logger.addHandler(StreamHandler())
logger.setLevel(logging.INFO)

