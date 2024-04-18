# app/routes.py

import socket
from app import app
from datetime import datetime, timedelta
import random
from flask import render_template

@app.route('/')
def index():
    # Información del nodo
    node_name = "Nodo 1"  # Reemplaza esto con el nombre real del nodo

    # Obtener la dirección IP del dispositivo
    ip_address = socket.gethostbyname(socket.gethostname())

    # Obtener la hora actual del sistema
    system_time = datetime.now()

    # Generar un número aleatorio de segundos entre 60 y 120
    random_seconds = random.randint(60, 120)

    # Decidir aleatoriamente si sumar o restar los segundos
    add_or_subtract = random.choice([True, False])

    # Sumar o restar los segundos a la hora actual
    if add_or_subtract:
        simulated_time = system_time + timedelta(seconds=random_seconds)
    else:
        simulated_time = system_time - timedelta(seconds=random_seconds)

    # Formatear la hora simulada
    simulated_time_str = simulated_time.strftime('%H:%M:%S')

    return render_template('index.html', node_name=node_name, ip_address=ip_address, system_time=system_time.strftime('%H:%M:%S'), simulated_time=simulated_time_str)
