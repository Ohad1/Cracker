from flask import Flask
from master import Master


if __name__ == '__main__':
    master_app = Flask(__name__)
    master = Master(master_app,
                    3,
                    ['http://0.0.0.0:5001', 'http://0.0.0.0:5002', 'http://0.0.0.0:5003'])
    master.run(host='0.0.0.0', port=5000)
