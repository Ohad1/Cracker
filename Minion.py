from flask import request

from FlaskAppWrapper import FlaskAppWrapper
from HashCracker import HashCracker

class Minion(FlaskAppWrapper):
    def __init__(self, app, **configs):
        super().__init__(app, **configs)
        self.add_endpoint('/crack', 'crack', self.crack)
        self.add_endpoint('/index', 'index', self.index)

    def crack(self):
        range_start = int(request.args.get('range_start'))
        range_end = int(request.args.get('range_end'))
        hash_str = request.args.get('hash_str')
        hash_cracker = HashCracker(range_start, range_end, hash_str)
        phone_number = hash_cracker.crack()
        if phone_number:
            res = {'phone_number': phone_number}
            return res, 200
        else:
            res = {'error': 'Hash not found'}
            return res, 400
