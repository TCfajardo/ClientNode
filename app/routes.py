import os
import random
import socket
from datetime import datetime, time, timedelta

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO

from app import app, socketio

load_dotenv()

current_simulated_time = datetime.now().strftime('%H:%M:%S')

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

@socketio.on('current_simulated_time')
def handle_current_simulated_time():
    global current_simulated_time
    try:
        # Obtener la hora simulada del frontend
        simulated_time_str = current_simulated_time.strftime('%H:%M:%S')

        # Analizar la hora simulada con el formato de 12 horas
        current_simulated_time = datetime.strptime(simulated_time_str, '%I:%M:%S %p').time()
        print("Hora simulada actualizada (formato de 12 horas):", current_simulated_time)
    except ValueError:
        try:
            # Intentar analizar la hora simulada con el formato de 24 horas si falla el formato de 12 horas
            current_simulated_time = datetime.strptime(simulated_time_str, '%H:%M:%S').time()
            print("Hora simulada actualizada (formato de 24 horas):", current_simulated_time)
        except ValueError as e:
            print("Error al analizar la hora simulada:", e)




# Método para recibir la hora del coordinador
@socketio.on('coordinator_time')
def handle_coordinator_time(coordinator_received_time):
    global coordinator_time, current_simulated_time
    
    # Limpiar la cadena antes de analizarla
    cleaned_time_str = coordinator_received_time.replace('\xa0', '')
    
    try:
        # Analizar la hora del coordinador con el formato correcto
        coordinator_time = time.fromisoformat(cleaned_time_str)
        print('Hora del coordinador recibida:', coordinator_time)
        print('Hora simulada:', current_simulated_time)
        calculate_time_difference()
    except ValueError as e:
        print('Error al analizar la hora del coordinador:', e)


def calculate_time_difference():
    global current_simulated_time, coordinator_time
    if current_simulated_time is not None and coordinator_time is not None:
        # Obtener la fecha actual para agregarla a las horas simuladas
        current_date = datetime.now().date()
        # Convertir las horas simuladas y de coordinador en objetos datetime completos
        current_simulated_datetime = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=int(current_simulated_time.split(':')[0]), minutes=int(current_simulated_time.split(':')[1]), seconds=int(current_simulated_time.split(':')[2]))
        coordinator_datetime = datetime.combine(current_date, coordinator_time)
        # Calcular la diferencia entre las horas simuladas y de coordinador
        time_difference = coordinator_datetime - current_simulated_datetime
        print('Diferencia entre la hora simulada y la hora del coordinador:', time_difference)
        # Obtener el puerto del archivo .env
        node_port = os.getenv('NODE_PORT', '5000')  # Valor predeterminado si NODE_PORT no está definido en el archivo .env
        # Construir la URL del nodo
        node_url = f'http://localhost:{node_port}'
        # Emitir la diferencia calculada como un evento de socket
        # También enviar la URL del nodo
        socketio.emit('time_difference', {'difference': time_difference.total_seconds(), 'node_url': node_url})  # Convertir a segundos
        # Llamar a la función para actualizar la hora simulada
        updateSimulatedTime(time_difference.total_seconds())
    else:
        print('No se puede calcular la diferencia porque la hora simulada o la hora del coordinador es nula.')

def updateSimulatedTime(difference_seconds):
    global current_simulated_time
    try:
        # Convertir la diferencia de tiempo a un objeto timedelta
        time_difference = timedelta(seconds=difference_seconds)
        # Obtener la fecha actual
        current_date = datetime.now().date()
        # Crear un objeto datetime combinando la fecha actual y la hora simulada actual
        current_simulated_datetime = datetime.combine(current_date, current_simulated_time)
        # Calcular la nueva hora simulada sumando la diferencia de tiempo
        new_simulated_datetime = current_simulated_datetime + time_difference
        # Actualizar la hora simulada
        current_simulated_time = new_simulated_datetime.time()
        print('Hora simulada actualizada:', current_simulated_time.strftime('%H:%M:%S'))
    except Exception as e:
        print('Error al actualizar la hora simulada:', e)
