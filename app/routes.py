import os
import random
import socket
from datetime import datetime, time, timedelta

from flask import Flask, render_template
from flask_socketio import SocketIO

from app import app, socketio

# Variable global para almacenar la hora recibida del coordinador
coordinator_time = None

# Variable global para almacenar la hora simulada
simulated_start_time = datetime.now().strftime('%H:%M:%S')

# Convertir la hora simulada a objeto datetime.time
simulated_start_time = datetime.strptime(simulated_start_time, '%H:%M:%S').time()

@app.route('/')
def index():
    global simulated_start_time
    node_name = os.getenv('NODE_NAME', 'Nodo1')
    ip_address = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
    system_time = datetime.now()

    # Si no hay hora simulada inicial, generarla
    if simulated_start_time is None:
        random_seconds = random.randint(60, 120)
        add_or_subtract = random.choice([True, False])

        if add_or_subtract:
            simulated_start_time = system_time + timedelta(seconds=random_seconds)
        else:
            simulated_start_time = system_time - timedelta(seconds=random_seconds)

    # Emitir la hora simulada a través del socket para que se actualice en el frontend
    socketio.emit('simulated_time', simulated_start_time.strftime('%H:%M:%S'))

    # Pasar simulated_start_time como parte del contexto
    return render_template(
        'index.html', 
        node_name=node_name, 
        ip_address=ip_address,
        system_time=system_time.strftime('%H:%M:%S'),
        simulated_time=simulated_start_time.strftime('%H:%M:%S')
    )

# Método para recibir la hora del coordinador
@socketio.on('coordinator_time')
def handle_coordinator_time(coordinator_received_time):
    global coordinator_time, simulated_start_time
    
    # Limpiar la cadena antes de analizarla
    cleaned_time_str = coordinator_received_time.replace('\xa0', '')
    
    try:
        # Analizar la hora del coordinador con el formato correcto
        coordinator_time = time.fromisoformat(cleaned_time_str)
        print('Hora del coordinador recibida:', coordinator_time)
        print('Hora simulada:', simulated_start_time)
        calculate_time_difference()
    except ValueError as e:
        print('Error al analizar la hora del coordinador:', e)

def calculate_time_difference():
    global simulated_start_time, coordinator_time
    if simulated_start_time is not None and coordinator_time is not None:
        # Obtener la fecha actual para agregarla a las horas simuladas
        current_date = datetime.now().date()

        # Convertir las horas simuladas y de coordinador en objetos datetime completos
        simulated_datetime = datetime.combine(current_date, simulated_start_time)
        coordinator_datetime = datetime.combine(current_date, coordinator_time)

        # Calcular la diferencia entre las horas simuladas y de coordinador
        time_difference = coordinator_datetime- simulated_datetime
        print('Diferencia entre la hora simulada y la hora del coordinador:', time_difference)

        # Emitir la diferencia calculada como un evento de socket
        socketio.emit('time_difference', {'difference': time_difference.total_seconds()})  # Convertir a segundos

    else:
        print('No se puede calcular la diferencia porque la hora simulada o la hora del coordinador es nula.')