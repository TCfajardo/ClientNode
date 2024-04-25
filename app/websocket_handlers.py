from app import socketio

@socketio.on('connect')
def on_connect():
    print('Cliente conectado al servidor WebSocket')
    socketio.emit('join_vue_clients')

@socketio.on('some_event')
def handle_some_event(data):
    print('Evento recibido:', data)

@socketio.on('log_message')
def handle_log_message(message):
    print(f'Log recibido: {message}')
    socketio.emit('log_message', message)