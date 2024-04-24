import os

from dotenv import load_dotenv

load_dotenv()

from app import app, socketio

port = int(os.getenv('NODE_PORT', 5001))
host = os.getenv('NODE_IP', '127.0.0.1')
socketio.run(app, host=host, port=port, debug=True)