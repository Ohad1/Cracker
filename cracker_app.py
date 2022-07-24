import json
import multiprocessing
from Runners.run_master import run_master


def cracker_app():
    with open('config_prod.json') as config_json:
        config = json.load(config_json)
    master_proc = multiprocessing.Process(target=run_master, args=('master', config))
    master_proc.start()


if __name__ == '__main__':
    cracker_app()
