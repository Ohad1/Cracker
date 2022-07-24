from flask import Flask
from Minion import Minion
import sys


def run_minion(args):
    if len(args) != 2:
        print('Invalid number of parameters')
        exit(1)
    name, url = args
    host, port = url.split(':')
    minion_app = Flask(name)
    minion_app.debug = True
    minion = Minion(minion_app)
    minion.run(host=host, port=port, threaded=True)


if __name__ == '__main__':
    run_minion(sys.argv[1:])
