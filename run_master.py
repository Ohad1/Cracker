import json

from flask import Flask
from Master import Master
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Invalid number of parameters')
        exit(1)
    name, url = sys.argv[1:]
    host, port = url.split(':')
    master_app = Flask(name)
    master_app.debug = True
    with open('config_prod.json') as config_json:
        config = json.load(config_json)
    master = Master(master_app,
                    config['default_num_of_minions'],
                    config['minion_urls'])
    master.run(host=host, port=port, threaded=True)
