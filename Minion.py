from flask import request
from FlaskAppWrapper import FlaskAppWrapper
from HashCracker import HashCracker
import log


class Minion(FlaskAppWrapper):
    def __init__(self, app, **configs):
        super().__init__(app, **configs)
        self.hash_uuid_to_cracker = {}
        self.add_endpoint('/crack', 'crack', self.crack)
        self.add_endpoint('/stop', 'stop', self.stop)

    def crack(self):
        range_start = int(request.args.get('range_start'))
        range_end = int(request.args.get('range_end'))
        hash_str = request.args.get('hash_str')
        hash_uuid = request.args.get('hash_uuid')
        log.logger.debug(f'{hash_str = }, {range_start = }, {range_end = }')
        hash_cracker = HashCracker(range_start, range_end, hash_str)
        self.hash_uuid_to_cracker[hash_uuid] = hash_cracker
        phone_number = hash_cracker.crack()
        if phone_number:
            res = {'phone_number': phone_number}
            return res, 200
        else:
            res = {'error': 'Hash not found'}
            return res, 400

    def stop(self):
        hash_uuid = request.args.get('hash_uuid')
        if hash_uuid not in self.hash_uuid_to_cracker:
            log.logger.error(f'No such hash UUID: {hash_uuid}')
            res = {'error': f'No such hash UUID: {hash_uuid}'}
            return res, 400
        log.logger.error(f'Stop cracker: {hash_uuid}')
        self.hash_uuid_to_cracker[hash_uuid].stop()
