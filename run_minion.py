from flask import Flask
from Minion import Minion
import sys
# from log import logger
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Invalid number of parameters')
        exit(1)
    name, url = sys.argv[1:]
    host, port = url.split(':')
    minion_app = Flask(name)
    minion_app.debug = True
    minion = Minion(minion_app)
    minion.run(host=host, port=port, threaded=True)
