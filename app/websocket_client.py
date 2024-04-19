import websocket


def on_message(ws, message):
    print(f"Mensaje recibido del servidor: {message}")

def on_error(ws, error):
    print(f"Error en la conexión: {error}")

def on_close(ws):
    print("Conexión cerrada")

def on_open(ws):
    print("Conexión establecida")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:3000",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
