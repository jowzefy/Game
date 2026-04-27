from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock
from kivy.clock import mainthread

class Lobby(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.players_label = Label(text="Players: ")
        self.add_widget(self.players_label)

    def on_enter(self):
        app = App.get_running_app()
        app.client.callback = self.handle_message
        # Request player list? Not needed if server sends it on join
        Clock.schedule_once(self.update_ui, 0.5)

    def update_ui(self, dt):
        app = App.get_running_app()
        self.players_label.text = f"Room: {app.room_code} - Players: {', '.join(app.players)}"
@mainthread
def handle_message(self, msg):
    app = App.get_running_app()
    msg_type = msg.get("type")
    if msg_type == "room_created":
        app.room_code = msg["room_code"]
        self.status.text = f"Room created: {app.room_code}"
        app.sm.current = "lobby"
    elif msg_type == "player_joined":
        app.sm.current = "lobby"
    elif msg_type == "error":
        self.status.text = msg["message"]
