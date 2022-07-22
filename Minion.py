from FlaskAppWrapper import FlaskAppWrapper
from HashCracker import HashCracker


class Minion(FlaskAppWrapper):
    def __init__(self, app, **configs):
        super().__init__(app, **configs)
        self.add_endpoint('/crack', 'crack', self.crack)

    def crack(self, hash_range, hash_str):
        hash_cracker = HashCracker(hash_range, hash_str)
        phone_number = hash_cracker.crack()
        if phone_number:
            return phone_number, 200
        else:
            return 'Hash not found', 400
