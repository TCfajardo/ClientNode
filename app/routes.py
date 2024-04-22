# routes.py

import os
import random
import socket
from datetime import datetime, timedelta

from flask import Flask, render_template

from app import app, socketio


@app.route('/')
def index():
    node_name = os.getenv('NODE_NAME', 'Nodo1')
    ip_address = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
    system_time = datetime.now().strftime('%H:%M:%S')
    random_seconds = random.randint(60, 120)
    add_or_subtract = random.choice([True, False])
    if add_or_subtract:
        simulated_time = (datetime.now() + timedelta(seconds=random_seconds)).strftime('%H:%M:%S')
    else:
        simulated_time = (datetime.now() - timedelta(seconds=random_seconds)).strftime('%H:%M:%S')

    return render_template('index.html', node_name=node_name, ip_address=ip_address, system_time=system_time, simulated_time=simulated_time)

# Endpoint para recibir la hora del coordinador
@socketio.on('coordinator_time')
def handle_coordinator_time(coordinator_time):
    print('Hora del coordinador recibida:', coordinator_time)
    coordinator_time = datetime.strptime(coordinator_time, '%d/%m/%Y, %I:%M:%S %p')
    simulated_time = datetime.now() - coordinator_time
    print('Diferencia entre la hora simulada y la hora del coordinador:', simulated_time)
    # Aquí puedes emitir la diferencia a través de WebSocket si es necesario
    # socketio.emit('difference', simulated_time)
