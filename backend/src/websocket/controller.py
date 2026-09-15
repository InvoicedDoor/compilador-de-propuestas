from flask_sock import Sock

sock = Sock()

@sock.route("/ws")
def websocket(ws):
    ws.send("Websocket conectado.")
    while True:
        message = ws.receive()

        if message is None:
            break

        ws.send(f"Servidor recibió: {message}")

@sock.route("/ws/approve-project/<project_id:int>")
def approve_project_controller(project_id):
    try:
        pass
    except:
        pass