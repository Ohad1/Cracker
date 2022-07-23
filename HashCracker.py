import hashlib
import log


class HashCracker:
    NUMBER_SIZE = 8

    def __init__(self, start, end, hash_str):
        self.start = start
        self.end = end
        self.hash_str = hash_str
        self.is_running = True

    def get_phone_number(self, num):
        filled_num = str(num).zfill(self.NUMBER_SIZE)
        return f'05{filled_num[0]}-{filled_num[1:]}'

    def crack(self):
        for num in range(self.start, self.end):
            if not self.is_running:
                log.logger.debug(f'Cracker terminated')
                return None
            phone_number = self.get_phone_number(num)
            encoded_phone_number = hashlib.md5(phone_number.encode()).hexdigest()
            log.logger.debug(f'{phone_number = }, {encoded_phone_number = }, {self.hash_str = }')
            if encoded_phone_number == self.hash_str:
                return phone_number
        log.logger.debug(f'{self.hash_str} not found in range({self.start}, {self.end})')
        return None

    def stop(self):
        self.is_running = False
