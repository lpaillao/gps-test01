# backend/app.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import threading
import socket
import json
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Almacenamiento en memoria para los datos del GPS
gps_data = {}

def parse_gps_data(data):
    # Ejemplo de parsing, ajusta según el formato real de tu GPS J16
    parts = data.split(',')
    if len(parts) < 8:
        return None
    return {
        'imei': parts[0],
        'timestamp': datetime.now().isoformat(),
        'latitude': float(parts[4]),
        'longitude': float(parts[5]),
        'speed': float(parts[6]),
        'direction': float(parts[7])
    }

def handle_gps_connection(conn, addr):
    logger.info(f"Nueva conexión GPS desde {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                parsed_data = parse_gps_data(data.decode().strip())
                if parsed_data:
                    imei = parsed_data['imei']
                    gps_data[imei] = parsed_data
                    socketio.emit('gps_update', parsed_data)
                    logger.info(f"Datos GPS recibidos: {parsed_data}")
            except Exception as e:
                logger.error(f"Error al procesar datos GPS: {str(e)}")

def start_gps_server():
    host = '0.0.0.0'  # Escucha en todas las interfaces
    port = 6006

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        logger.info(f"Servidor GPS escuchando en {host}:{port}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_gps_connection, args=(conn, addr))
            thread.start()

@app.route('/gps', methods=['GET'])
def get_gps_data():
    return jsonify(gps_data)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Iniciar el servidor GPS en un hilo separado
    gps_thread = threading.Thread(target=start_gps_server)
    gps_thread.start()

    # Iniciar el servidor Flask
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Iniciando servidor Flask en 0.0.0.0:{port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
