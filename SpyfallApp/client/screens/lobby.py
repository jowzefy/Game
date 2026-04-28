from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import mainthread, Clock

class Lobby(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.players_label = Label(text="Players: ")
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(self.players_label)
        
        self.start_btn = Button(text="Start Game", size_hint=(1, 0.2))
        self.start_btn.bind(on_press=self.start_game)
        self.layout.add_widget(self.start_btn)
        
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        app.client.callback = self.handle_message
        # اطمینان از اینکه players_label وجود داره
        if hasattr(self, 'players_label'):
            self.players_label.text = "Players: waiting..."
        Clock.schedule_once(self.update_ui, 0.5)

    def update_ui(self, dt):
        app = App.get_running_app()
        if hasattr(self, 'players_label') and hasattr(app, 'players'):
            self.players_label.text = f"Room Code: {app.room_code} \n\n Players: {', '.join(app.players)}"

    def start_game(self, instance):
        app = App.get_running_app()
        app.client.send("start_game")

    @mainthread
    def handle_message(self, msg):
        app = App.get_running_app()
        msg_type = msg.get("type")
        if msg_type == "player_joined":
            app.players = msg["players"]
            self.update_ui(0)
        elif msg_type == "your_role":
            app.my_role = msg["role"]
            app.location = msg.get("location")
            app.sm.current = "role_reveal"
        elif msg_type == "error":
            app.sm.current = "main_menu"
