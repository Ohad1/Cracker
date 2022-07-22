from HashValidator import HashValidator
from flask import Flask, request
import json

master_app = Flask(__name__)


@master_app.get('/crack')
def crack():
    hashes_arg = request.args.get('hashes')
    hashes = hashes_arg.split(',')
    hash_validator = HashValidator(hashes)
    if not hash_validator.validate_hashes():
        return 'Invalid hashes provided', 400
    return json.dumps(hashes, indent=4), 200


class Master:
    def __init__(self, host_url, default_num_of_minions, minions_urls):
        self.host_url = host_url
        self.default_num_of_minions = default_num_of_minions
        self.minions_urls = minions_urls

    def start_app(self):
        master_app.run(debug=True)
