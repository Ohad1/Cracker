import json

from flask import Flask
from Master import Master
import sys


def run_master(name, config):
    host, port = config['server_url'].split(':')
    master_app = Flask(name)
    master = Master(master_app,
                    config['default_num_of_minions'],
                    config['minion_urls'],
                    config['db_conf'],
                    config['cache_size'],
                    config['server_url'])
    master.run(host=host, port=port, threaded=True)


if __name__ == '__main__':
    run_master(sys.argv[1:])
