from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import mainthread

class Voting(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

    def on_enter(self):
        self.layout.clear_widgets()
        app = App.get_running_app()
        app.client.callback = self.handle_message
        self.layout.add_widget(Label(text="Vote for who you think is the spy:"))
        for player in app.players:
            if player != app.player_id:
                btn = Button(text=player, size_hint=(1, 0.2))
                btn.bind(on_press=lambda x, p=player: self.cast_vote(p))
                self.layout.add_widget(btn)

    def cast_vote(self, target):
        app = App.get_running_app()
        app.client.send("cast_vote", {"target": target})
        self.layout.add_widget(Label(text=f"You voted for {target}"))

    @mainthread
    def handle_message(self, msg):
        app = App.get_running_app()
        if msg.get("type") == "vote_result":
            app.vote_result = msg
            app.sm.current = "result"
