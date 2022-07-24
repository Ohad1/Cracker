from flask import request
from FlaskAppWrapper.FlaskAppWrapper import FlaskAppWrapper
from HashCracker import HashCracker
from Logger.crack_logger import logger


class Minion(FlaskAppWrapper):
    def __init__(self, app, **configs):
        super().__init__(app, **configs)
        self.name = app.name.upper()
        self.hash_uuid_to_cracker = {}
        self.add_endpoint('/crack', 'crack', self.crack)
        self.add_endpoint('/stop', 'stop', self.stop)

    def crack(self):
        range_start = int(request.args.get('range_start'))
        range_end = int(request.args.get('range_end'))
        hash_str = request.args.get('hash_str')
        hash_uuid = request.args.get('hash_uuid')
        logger.debug(f'[{self.name}] {hash_str = }, {range_start = }, {range_end = }, {hash_uuid = }')
        hash_cracker = HashCracker(range_start, range_end, hash_str, hash_uuid)
        self.hash_uuid_to_cracker[hash_uuid] = hash_cracker
        ret = hash_cracker.crack()
        if isinstance(ret, str):
            res = {'phone_number': ret}
            logger.debug(f'[{self.name}] {res = }')
            return res, 200
        elif isinstance(ret, dict):
            logger.debug(f'[{self.name}] {ret = }')
            return ret, 200
        else:
            res = {'error': f'Hash not found {hash_str = }'}
            logger.debug(f'[{self.name}] {res = }')
            return res, 400

    def stop(self):
        hash_uuid = request.args.get('hash_uuid')
        if hash_uuid not in self.hash_uuid_to_cracker:
            logger.error(f'[{self.name}] No such hash UUID: {hash_uuid}')
            res = {'error': f'No such hash UUID: {hash_uuid}'}
            return res, 400
        logger.info(f'[{self.name}] Stop cracker: {hash_uuid}')
        self.hash_uuid_to_cracker[hash_uuid].stop()
        return {'message': f'Cracker {hash_uuid} was stopped'}, 200
