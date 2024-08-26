import socket
import time
import random

# Configuración del servidor
HOST = '127.0.0.1'  # localhost
PORT = 6006  # El mismo puerto que configuraste en tu servidor

# Función para generar datos GPS simulados
def generate_gps_data():
    imei = "123456789012345"  # IMEI simulado
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    speed = random.uniform(0, 120)
    direction = random.uniform(0, 360)
    
    # Formato: IMEI,estado,fecha,hora,latitud,longitud,velocidad,dirección
    return f"{imei},A,{time.strftime('%Y%m%d,%H%M%S')},{latitude:.6f},{longitude:.6f},{speed:.2f},{direction:.2f}"

# Conexión al servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Conectado al servidor {HOST}:{PORT}")
    
    try:
        while True:
            data = generate_gps_data()
            s.sendall(data.encode())
            print(f"Datos enviados: {data}")
            time.sleep(5)  # Envía datos cada 5 segundos
    except KeyboardInterrupt:
        print("Simulación terminada por el usuario")