from flask import Flask
from Minion import Minion
import sys


def run_minion(name, url):
    host, port = url.split(':')
    minion_app = Flask(name)
    minion = Minion(minion_app)
    minion.run(host=host, port=port, threaded=True)


if __name__ == '__main__':
    run_minion(sys.argv[1:])
