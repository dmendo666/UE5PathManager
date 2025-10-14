import unreal

# Importar y ejecutar el servidor WebSocket
# try:
#     import websocket_server
#     print("Servidor WebSocket iniciado exitosamente")
#     unreal.log("WebSocket server initialized successfully")
# except ImportError as e:
#     print(f"Error importando websocket_server: {e}")
#     unreal.log_error(f"Error importing websocket_server: {e}")
# except Exception as e:
#     print(f"Error iniciando WebSocket server: {e}")
#     unreal.log_error(f"Error starting WebSocket server: {e}")


try:
    import json_blueprint
    print("json_blueprint iniciado exitosamente")
    unreal.log("json_blueprint initialized successfully")
except ImportError as e:
    print(f"Error importando json_blueprint: {e}")
    unreal.log_error(f"Error importing json_blueprint: {e}")
except Exception as e:
    print(f"Error iniciando json_blueprint: {e}")
    unreal.log_error(f"Error starting json_blueprint: {e}")