import json
import multiprocessing
from Runners.run_master import run_master
from pathlib import Path
import os


def cracker_app():
    config_path = os.path.join(Path(__file__).parent.parent, 'config.json')
    with open(config_path) as config_json:
        config = json.load(config_json)
    master_proc = multiprocessing.Process(target=run_master, args=('master', config))
    master_proc.start()


if __name__ == '__main__':
    cracker_app()
