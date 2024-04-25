import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": ""}})
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins='*')

from app import routes, websocket_handlers

if __name__ == '__main__':
    socketio.run(app, debug=True)