import os
import random
import socket
from datetime import datetime, time, timedelta

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO

from app import app, socketio

load_dotenv()

coordinator_time = None
simulated_start_time = None
node_time_difference = None
current_simulated_time = None

@app.route('/')
def index():
    global simulated_start_time

    node_name = os.getenv('NODE_NAME', 'Nodo1')
    ip_address = os.getenv('NODE_IP', 'localhost')
    system_time = datetime.now()

    if simulated_start_time is None:
        random_seconds = random.randint(60, 200)
        add_or_subtract = random.choice([True, False])
        if add_or_subtract:
            simulated_start_time = system_time + timedelta(seconds=random_seconds)
        else:
            simulated_start_time = system_time - timedelta(seconds=random_seconds)
    socketio.emit('simulated_time', simulated_start_time.strftime('%H:%M:%S'))
    print("Simulated start:", simulated_start_time.strftime('%H:%M:%S'))
    print("System start:", system_time.strftime('%H:%M:%S'))
    
    return render_template(
        'index.html',
        node_name=node_name,
        ip_address=ip_address,
        system_time=system_time.strftime('%H:%M:%S'),
        simulated_time=simulated_start_time.strftime('%H:%M:%S')
    )
    
@socketio.on('current_simulated_time')
def update_simulated_time(formatted_time):
    global current_simulated_time, simulated_start_time
    try:
        current_simulated_time = datetime.strptime(formatted_time, '%H:%M:%S').time()  

        simulated_start_time_str = simulated_start_time.strftime('%H:%M:%S')

        print("Valor inicial de current_simulated_time:", simulated_start_time_str)
        print("Simulated time received:", current_simulated_time.strftime('%H:%M:%S'))
    except ValueError:
        print("Error parsing simulated time:", formatted_time)


# Método para recibir la hora del coordinador
@socketio.on('coordinator_time')
def handle_coordinator_time(coordinator_received_time):
    global coordinator_time, current_simulated_time
    
    # Limpiar la cadena antes de analizarla
    cleaned_time_str = coordinator_received_time.replace('\xa0', '')
    
    try:
        # Analizar la hora del coordinador con el formato correcto
        coordinator_time = time.fromisoformat(cleaned_time_str)
        print('-------Hora del coordinador recibida:', coordinator_time)
        print('-------Hora actual simulada:', current_simulated_time)
        log_message = f'Hora del coordinador recibida: {coordinator_time}'
        socketio.emit('log_message', log_message) 
        calculate_time_difference()
    except ValueError as e:
        print('Error al analizar la hora del coordinador:', e)


def calculate_time_difference():
    global current_simulated_time, coordinator_time
    if current_simulated_time is not None and coordinator_time is not None:
        current_date = datetime.now().date()
        
        current_simulated_datetime = datetime.combine(current_date, current_simulated_time)
        print('-------------------Hora actual con date:', current_simulated_datetime)
        print('-------------------Hora actual con date:', current_simulated_datetime)
        
        coordinator_datetime = datetime.combine(current_date, coordinator_time)
        # Calcular la diferencia entre las horas simuladas y de coordinador
        time_difference = coordinator_datetime - current_simulated_datetime
        
        print('Diferencia entre la hora simulada y la hora del coordinador:', time_difference)
        total_seconds = abs(time_difference.total_seconds())
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        # Formato legible para el log
        formatted_time_difference = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        # Construir el mensaje de log
        difference_log = f"Diferencia entre la hora del nodo y la hora del coordinador: {formatted_time_difference}"
        
        # Emitir el mensaje de log
        socketio.emit('log_message', difference_log)

        # Obtener el puerto del archivo .env
        node_port = os.getenv('NODE_PORT', '5000') 
        ip_address = os.getenv('NODE_IP', 'localhost')
        # Construir la URL del nodo
        node_url = f'http://{ip_address}:{node_port}'
        # Emitir la diferencia calculada como un evento de socket
        # También enviar la URL del nodo
        socketio.emit('time_difference', {'difference': time_difference.total_seconds(), 'node_url': node_url})
        # Llamar a la función para actualizar la hora simulada
    else:
        print('No se puede calcular la diferencia porque la hora simulada o la hora del coordinador es nula.')


# Método para recibir la diferencia de tiempo de cada nodo respecto al promedio
@socketio.on('node_time_difference')
def handle_node_time_difference(node_difference):
    global node_time_difference
    try:
        # Obtener la diferencia de tiempo del nodo respecto al promedio
        node_time_difference = node_difference['difference']
        print("Valor actual de current_simulated_time:", current_simulated_time)
        print('Diferencia de tiempo recibida desde el nodo:', node_time_difference)
        # Llamar a la función para actualizar la hora simulada después de recibir la diferencia de tiempo del nodo
        update_simulated_time()
        # Aquí puedes realizar cualquier acción adicional que necesites con la diferencia de tiempo recibida
    except Exception as e:
        print('Error al manejar la diferencia de tiempo del nodo:', e)

def update_simulated_time():
    global current_simulated_time, node_time_difference
    try:
        if node_time_difference is not None:
            # Convertir la diferencia de tiempo a milisegundos
            time_difference_ms = node_time_difference * 1000
            
            # Obtener la fecha y hora actual
            current_datetime = datetime.now()
            
            # Crear un objeto datetime con la fecha actual y la hora simulada
            current_simulated_datetime = datetime.combine(current_datetime.date(), current_simulated_time)
            
            # Calcular la nueva hora simulada sumando los milisegundos de la diferencia de tiempo
            new_simulated_datetime = current_simulated_datetime + timedelta(milliseconds=time_difference_ms)
            
            # Actualizar la hora simulada
            current_simulated_time = new_simulated_datetime.time()
            
            print('Hora simulada actualizada:', current_simulated_time.strftime('%H:%M:%S'))
    except Exception as e:
        print('Error al actualizar la hora simulada:', e)
        
