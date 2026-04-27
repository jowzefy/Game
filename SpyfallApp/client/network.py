import json
import threading
from websocket import WebSocketApp
from kivy.clock import mainthread
class GameClient:
    def __init__(self):
    
        self.ws = None
        self.callback = None
        self.connected = False

    def connect(self, url):
        self.ws = WebSocketApp(url,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    @mainthread
    def on_open(self, ws):
        self.connected = True
        if self.callback:
            self.callback({"type": "connection", "status": "connected"})

    @mainthread
    def on_message(self, ws, message):
        data = json.loads(message)
        if self.callback:
            self.callback(data)

    @mainthread
    def on_error(self, ws, error):
        if self.callback:
            self.callback({"type": "error", "message": str(error)})

    def on_close(self, ws, *args):
        self.connected = False
        if self.callback:
            self.callback({"type": "connection", "status": "disconnected"})

    def send(self, action, payload=None):
        if self.ws and self.connected:
            msg = json.dumps({"action": action, "payload": payload or {}})
            self.ws.send(msg)
    def send(self, action, payload=None):
        msg = {"action": action, "payload": payload or {}}
        print(f"🔵 CLIENT SENDING: {msg}")  # ← اینو اضافه کن
        if self.ws and self.connected:
            self.ws.send(json.dumps(msg))
        else:
            print("🔴 CLIENT NOT CONNECTED!")
