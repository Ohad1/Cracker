from HashValidator import HashValidator
from flask import Flask, request
import json
from FlaskAppWrapper import FlaskAppWrapper
from Minion import Minion
from HashCracker import HashCracker

class Master(FlaskAppWrapper):
    def __init__(self, app, default_num_of_minions, minions_urls, **configs):
        self.default_num_of_minions = default_num_of_minions
        self.minions_urls = minions_urls
        self.minions = []
        super().__init__(app, **configs)
        self.add_endpoint('/crack', 'crack', self.crack)
        for i, url in enumerate(self.minions_urls[:self.default_num_of_minions]):
            self.minions.append(Minion(Flask(f'minion_{i + 1}'), host=url))

    def crack(self):
        hashes_arg = request.args.get('hashes')
        hashes = hashes_arg.split(',')
        hash_validator = HashValidator(hashes)
        if not hash_validator.validate_hashes():
            return 'Invalid hashes provided', 400
        res = []
        for hash_str in hashes:
            hash_cracker = HashCracker(range(0, 10 ** 8), hash_str)
            res.append(hash_cracker.crack())
        return '\n'.join(res), 200
