import serial
import asyncio
import websockets

# Raspberry Pi Serial Port Configuration
SERIAL_PORT = '/dev/ttyS0'  # Raspberry Pi serial port
BAUD_RATE = 9600

# WebSocket Configuration
HOST = '0.0.0.0'  # Bind to all network interfaces
PORT = 6789

async def serial_to_websocket():
    # Open serial port
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=10) as ser:
        async with websockets.serve(send_serial_data, HOST, PORT):
            print(f"WebSocket server started on ws://{HOST}:{PORT}")
            await asyncio.Future()  # Keep server running

async def send_serial_data(websocket, path):
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=10) as ser:
        while True:
            data = ser.readline().decode('utf-8').strip()  # Read serial data
            if data:
                print(f"Received from serial: {data}")
                await websocket.send(data)  # Send data to client
            await asyncio.sleep(0.1)  # Avoid overloading the server

if __name__ == "__main__":
    try:
        asyncio.run(serial_to_websocket())
    except KeyboardInterrupt:
        print("Server stopped.")
