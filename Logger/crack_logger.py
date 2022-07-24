import logging
from multiprocessing_logging import install_mp_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s| %(levelname)5s| %(filename)s:%(lineno)s - %(funcName)s()] %(message)s')
handler = logging.FileHandler('cracker_app.log')
handler.setFormatter(formatter)

# this bit will make sure you won't have
# duplicated messages in the output
if not logger.handlers:
    logger.addHandler(handler)

install_mp_handler()
