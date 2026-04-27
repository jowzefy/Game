from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import mainthread

class MainMenu(Screen):
    def init(self, **kwargs):
        super().init(**kwargs)
        self.status = Label(text="")  # اول status رو بساز
        self.build_ui()
        app = App.get_running_app()
        if hasattr(app, 'client'):
            app.client.callback = self.handle_message  # callback رو بذار

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(1, 1))
        layout.add_widget(Label(text="Spyfall", font_size=48, size_hint=(1, 0.2)))

        self.player_name = TextInput(hint_text="Your name", multiline=False, size_hint=(1, 0.1))
        layout.add_widget(self.player_name)

        self.room_code = TextInput(hint_text="Room code (for join)", multiline=False, size_hint=(1, 0.1))
        layout.add_widget(self.room_code)

        btn_create = Button(text="Create Room", size_hint=(1, 0.15))
        btn_create.bind(on_press=self.create_room)
        layout.add_widget(btn_create)

        btn_join = Button(text="Join Room", size_hint=(1, 0.15))
        btn_join.bind(on_press=self.join_room)
        layout.add_widget(btn_join)

        layout.add_widget(self.status)  # status قبلاً ساخته شده
        self.add_widget(layout)

    def create_room(self, instance):
        name = self.player_name.text.strip()
        if not name:
            self.status.text = "Enter a name"
            return
        app = App.get_running_app()
        app.player_id = name
        app.client.send("create_room", {"player_id": name})

    def join_room(self, instance):
        name = self.player_name.text.strip()
        code = self.room_code.text.strip().upper()
        if not name or not code:
            self.status.text = "Enter name and room code"
            return
        app = App.get_running_app()
        app.player_id = name
        app.client.send("join_room", {"player_id": name, "room_code": code})

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
