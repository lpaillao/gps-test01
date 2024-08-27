#!/bin/bash

# Nombre del script: start_gps_project.sh

# Navegar al directorio raíz del proyecto
cd /ruta/a/GPS01

# Función para iniciar el backend
start_backend() {
    echo "Iniciando el backend..."
    cd backend
    source venv/bin/activate  # Asumiendo que uses un entorno virtual
    pip install -r requirements.txt  # Asegurarse de que todas las dependencias están instaladas
    gunicorn --bind 0.0.0.0:5000 app:app --worker-class eventlet -w 1 --daemon
    cd ..
}

# Función para preparar y servir el frontend
prepare_and_serve_frontend() {
    echo "Preparando y sirviendo el frontend..."
    cd frontend
    npm install
    npm run build
    # Asumiendo que tienes Nginx instalado y configurado para servir la aplicación React
    sudo cp -r build/* /var/www/gps-project/
    sudo systemctl reload nginx
    cd ..
}

# Iniciar los servicios
start_backend
prepare_and_serve_frontend

echo "El sistema GPS está iniciando. Por favor, espera..."
echo "Backend corriendo en segundo plano con Gunicorn."
echo "Frontend servido a través de Nginx."

# Mantener el script en ejecución
tail -f /dev/null