import json

from flask import Flask
from Master import Master
import sys


def run_master(args):
    if len(args) != 2:
        print('Invalid number of parameters')
        exit(1)
    name, url = args
    host, port = url.split(':')
    master_app = Flask(name)
    master_app.debug = True
    with open('config_prod.json') as config_json:
        config = json.load(config_json)
    master = Master(master_app,
                    config['default_num_of_minions'],
                    config['minion_urls'],
                    config['db_conf'],
                    config['cache_size'],
                    url)
    master.run(host=host, port=port, threaded=True)


if __name__ == '__main__':
    run_master(sys.argv[1:])
