from flask import Flask, render_template
from datetime import datetime, timedelta
import random
import socket
import os
from app import app

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
