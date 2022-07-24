import hashlib
from Logger.crack_logger import logger


class HashCracker:
    NUMBER_SIZE = 8

    def __init__(self, start, end, hash_str, hash_uuid):
        self.start = start
        self.end = end
        self.hash_str = hash_str
        self.hash_uuid = hash_uuid
        self.is_running = True

    def get_phone_number(self, num):
        filled_num = str(num).zfill(self.NUMBER_SIZE)
        return f'05{filled_num[0]}-{filled_num[1:]}'

    def crack(self):
        logger.debug(f'[{self.hash_uuid}] Cracker started')
        for num in range(self.start, self.end):
            if not self.is_running:
                logger.debug(f'[{self.hash_uuid}] Cracker terminated. reached {num} in range({self.start}, {self.end})')
                return {'message': f'Cracker {self.hash_uuid} of hash {self.hash_str} was terminated before completion'}
            phone_number = self.get_phone_number(num)
            encoded_phone_number = hashlib.md5(phone_number.encode()).hexdigest()
            if encoded_phone_number == self.hash_str:
                logger.debug(f'[{self.hash_uuid}] Phone number found: {phone_number}')
                return phone_number
        logger.debug(f'[{self.hash_uuid}] {self.hash_str} not found in range({self.start}, {self.end})')
        return None

    def stop(self):
        self.is_running = False
