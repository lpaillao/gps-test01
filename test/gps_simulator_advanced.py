import socket
import time
import math
import sys

# Configuración del servidor
HOST = '127.0.0.1'  # localhost
PORT = 6006  # El mismo puerto que configuraste en tu servidor

# Configuración de la ruta circular
CENTER_LAT = 40.7128  # Latitud central (ejemplo: Nueva York)
CENTER_LON = -74.0060  # Longitud central
RADIUS = 0.01  # Radio del círculo en grados (aproximadamente 1 km)
SPEED = 0.001  # Velocidad de movimiento en grados por segundo

def generate_gps_data(angle):
    imei = "123456789012345"  # IMEI simulado
    latitude = CENTER_LAT + RADIUS * math.sin(angle)
    longitude = CENTER_LON + RADIUS * math.cos(angle)
    speed = SPEED * 111000  # Convertir a m/s (aproximadamente)
    direction = (angle * 180 / math.pi + 90) % 360  # Dirección tangente al círculo
    
    return f"{imei},A,{time.strftime('%Y%m%d,%H%M%S')},{latitude:.6f},{longitude:.6f},{speed:.2f},{direction:.2f}"

print(f"Intentando conectar a {HOST}:{PORT}")
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado exitosamente al servidor {HOST}:{PORT}")
        
        angle = 0
        try:
            while True:
                data = generate_gps_data(angle)
                s.sendall(data.encode())
                print(f"Datos enviados: {data}")
                time.sleep(1)  # Envía datos cada segundo
                angle += SPEED
                if angle >= 2 * math.pi:
                    angle -= 2 * math.pi
        except KeyboardInterrupt:
            print("Simulación terminada por el usuario")
except ConnectionRefusedError:
    print(f"Error: No se pudo conectar al servidor {HOST}:{PORT}")
    print("Asegúrate de que el servidor esté ejecutándose y escuchando en el puerto correcto.")
    sys.exit(1)
except Exception as e:
    print(f"Error inesperado: {e}")
    sys.exit(1)