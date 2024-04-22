import os

from app import app, socketio

if __name__ == '__main__':
    port = int(os.getenv('NODE_PORT', 5001))
    socketio.run(app, host='localhost', port=port, debug=True)

