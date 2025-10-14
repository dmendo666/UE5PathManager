import asyncio
import websockets
import threading
import unreal

class WebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.server = None
        self.running = False
        
    async def handle_client(self, websocket):
        """Maneja las conexiones de clientes WebSocket"""
        print(f"Cliente conectado desde {websocket.remote_address}")
        
        try:
            async for message in websocket:
                # Imprimir en la consola de Unreal Engine
                #print(f"Mensaje recibido: {message}")
                unreal.log(f"WebSocket mensaje: {message}")
                
                # Opcional: enviar confirmación al cliente
                await websocket.send(f"Mensaje recibido: {message}")
                
        except websockets.exceptions.ConnectionClosed:
            print("Cliente desconectado")
        except Exception as e:
            print(f"Error manejando cliente: {e}")
    
    async def start_server(self):
        """Inicia el servidor WebSocket"""
        try:
            self.server = await websockets.serve(
                self.handle_client, 
                self.host, 
                self.port
            )
            self.running = True
            print(f"Servidor WebSocket iniciado en ws://{self.host}:{self.port}")
            unreal.log(f"Servidor WebSocket iniciado en ws://{self.host}:{self.port}")
            
            # Mantener el servidor corriendo
            await self.server.wait_closed()
            
        except Exception as e:
            print(f"Error iniciando servidor: {e}")
            unreal.log_error(f"Error iniciando servidor WebSocket: {e}")
    
    def start_in_thread(self):
        """Inicia el servidor en un hilo separado"""
        def run_server():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.start_server())
        
        if not self.running:
            thread = threading.Thread(target=run_server, daemon=True)
            thread.start()
            return thread
    
    async def stop_server(self):
        """Detiene el servidor"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.running = False
            print("Servidor WebSocket detenido")

# Variable global para mantener referencia al servidor
websocket_server_instance = None

def start_websocket_server(host='localhost', port=8765):
    """Función para iniciar el servidor WebSocket"""
    global websocket_server_instance
    
    if websocket_server_instance is None or not websocket_server_instance.running:
        websocket_server_instance = WebSocketServer(host, port)
        thread = websocket_server_instance.start_in_thread()
        return websocket_server_instance
    else:
        print("El servidor WebSocket ya está corriendo")
        return websocket_server_instance

def stop_websocket_server():
    """Función para detener el servidor WebSocket"""
    global websocket_server_instance
    
    if websocket_server_instance and websocket_server_instance.running:
        # Nota: Para detener completamente necesitarías manejar el event loop
        print("Para detener el servidor, reinicia Unreal Engine")
        unreal.log("Para detener el servidor WebSocket, reinicia Unreal Engine")

# Auto-iniciar el servidor cuando se importa el módulo
if __name__ == "__main__":
    start_websocket_server()

# Iniciar automáticamente
print("Iniciando servidor WebSocket automáticamente...")
start_websocket_server()