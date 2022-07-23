import hashlib


class HashCracker:
    NUMBER_SIZE = 8

    def __init__(self, start, end, hash_str):
        self.start = start
        self.end = end
        self.hash_str = hash_str

    def get_phone_number(self, num):
        filled_num = str(num).zfill(self.NUMBER_SIZE)
        return f'05{filled_num[0]}-{filled_num[1:]}'

    def crack(self):
        for num in range(self.start, self.end):
            phone_number = self.get_phone_number(num)
            if hashlib.md5(phone_number.encode()).hexdigest() == self.hash_str:
                return phone_number
        return None

