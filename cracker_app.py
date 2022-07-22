from flask import Flask
from master import Master


if __name__ == '__main__':
    master_app = Flask(__name__)
    master = Master(master_app,
                    'http://127.0.0.1:5000',
                    3,
                    ['http://127.0.0.1:5001', 'http://127.0.0.1:5002', 'http://127.0.0.1:5003'])
    master.run()
