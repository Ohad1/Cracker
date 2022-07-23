import json

from flask import Flask
from master import Master
import sys
import subprocess


class ConnectionManager:
    def __init__(self, config):
        self.config = config
        subprocess.Popen(f'py run_master.py master {config["server_url"]}', shell=True)
        for i in range(config['default_num_of_minions']):
            subprocess.Popen(f'py run_minion.py minion_{i + 1} {config["minion_urls"][i]}', shell=True)


if __name__ == '__main__':
    with open('config_prod.json') as config_json:
        config = json.load(config_json)
    connection_manager = ConnectionManager(config)
