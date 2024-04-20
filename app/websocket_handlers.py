from app import socketio

@socketio.on('connect')
def on_connect():
    print('Cliente conectado al servidor WebSocket')

@socketio.on('some_event')
def handle_some_event(data):
    print('Evento recibido:', data)

# Otros manejadores de eventos
