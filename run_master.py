from flask import Flask
from master import Master
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Invalid number of parameters')
        exit(1)
    name, url = sys.argv[1:]
    host, port = url.split(':')
    master_app = Flask(name)
    master_app.debug = True
    master = Master(master_app,
                    1,
                    ['0.0.0.0:5001', '0.0.0.0:5002', '0.0.0.0:5003'])
    master.run(host=host, port=port)
