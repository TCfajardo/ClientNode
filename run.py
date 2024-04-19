# run.py

import os

from app import app

if __name__ == '__main__':
    node_port = int(os.getenv('NODE_PORT', 5001))
    print("Node Port:", node_port)

    app.run(host='localhost', port=node_port)
