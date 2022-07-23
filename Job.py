
from uuid import uuid4
import log


class Job:
    def __init__(self, hash_str, minion, hash_range):
        self.hash_str = hash_str
        self.minion_url = minion['url']
        self.start, self.end = hash_range
        self.name = f'JOB_{self.hash_str}_{self.start}_{self.end}'
        self.uuid = str(uuid4())
        self.is_done = False

    def done(self):
        self.is_done = True

    def get_termination_url(self):
        url = f'http://{self.minion_url}/stop?hash_uuid={self.uuid}'
        log.logger.info(f'[{self.name}] {url = }')
        return url

    def get_execution_url(self):
        url = f'http://{self.minion_url}/crack?hash_str={self.hash_str}&' \
               f'range_start={self.start}&' \
               f'range_end={self.end}&' \
               f'hash_uuid={self.uuid}'
        log.logger.info(f'[{self.name}] {url = }')
        return url

    def __str__(self):
        return str(self.__dict__)

