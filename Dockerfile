FROM python:3.8-slim

WORKDIR /app

COPY requeriments.txt requeriments.txt
# Usa una imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Expone el puerto en el que la aplicación Flask se ejecutará
EXPOSE 5003

# Define las variables de entorno
ENV NODE_PORT=5005
ENV NODE_NAME=Nodo5
ENV NODE_IP=localhost

# Ejecuta la aplicación Flask cuando se inicie el contenedor
CMD ["python", "run.py"]
