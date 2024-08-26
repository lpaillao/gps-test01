import React, { useState, useEffect, useCallback } from 'react';
import io from 'socket.io-client';

const SOCKET_SERVER_URL = process.env.REACT_APP_SOCKET_SERVER_URL || 'http://192.168.1.25:5000';
console.log('Conectando a:', SOCKET_SERVER_URL);

function App() {
  const [gpsData, setGpsData] = useState({});
  const [connectionStatus, setConnectionStatus] = useState('Desconectado');

  const connectSocket = useCallback(() => {
    console.log('Intentando conectar a:', SOCKET_SERVER_URL);
    const socket = io(SOCKET_SERVER_URL, {
      transports: ['websocket', 'polling'], // Intenta WebSocket primero, luego polling
      withCredentials: false,
    });

    socket.on('connect', () => {
      console.log('Conectado al servidor');
      setConnectionStatus('Conectado');
    });

    socket.on('connect_error', (error) => {
      console.error('Error de conexión:', error);
      setConnectionStatus('Error de conexión');
    });

    socket.on('disconnect', () => {
      console.log('Desconectado del servidor');
      setConnectionStatus('Desconectado');
    });

    socket.on('gps_update', (data) => {
      console.log('Datos GPS recibidos:', data);
      setGpsData(prevData => ({...prevData, [data.imei]: data}));
    });

    return socket;
  }, []);

  useEffect(() => {
    const socket = connectSocket();

    return () => {
      socket.disconnect();
    };
  }, [connectSocket]);
  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <h1 className="text-2xl font-semibold mb-5">Datos GPS J16</h1>
          <p className="mb-4">Estado: <span className={connectionStatus === 'Conectado' ? 'text-green-500' : 'text-red-500'}>{connectionStatus}</span></p>
          {Object.entries(gpsData).map(([imei, data]) => (
            <div key={imei} className="mb-4">
              <h2 className="text-xl font-semibold">IMEI: {imei}</h2>
              <pre className="bg-gray-100 p-4 rounded-md overflow-auto">
                {JSON.stringify(data, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;