# app/routes.py

import os
from dotenv import load_dotenv
import socket
from app import app
from datetime import datetime, timedelta
import random
from flask import render_template

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

@app.route('/')
def index():
    # Obtener el puerto del nodo desde la variable de entorno
    node_port = int(os.getenv('NODE_PORT', 5001))
    print("Node Port:", node_port)

    # Obtener el nombre del nodo desde la variable de entorno
    node_name = os.getenv('NODE_NAME', 'Nodo1')

    # Obtener la dirección IP del adaptador de LAN inalámbrica Wi-Fi
    ip_address = socket.gethostbyname_ex(socket.gethostname())[-1][-1]

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

    return render_template('index.html', node_name=node_name, ip_address=ip_address, system_time=system_time.strftime('%H:%M:%S'), simulated_time=simulated_time_str, node_port=node_port)
