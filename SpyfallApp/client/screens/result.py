from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock
from kivy.clock import mainthread

class Result(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.label = Label()
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        app.client.callback = self.handle_message
        # Show result if already received
        if hasattr(app, 'vote_result'):
            self.display_result(app.vote_result)

    def display_result(self, result):
        suspect = result.get("suspect")
        votes = result.get("votes", {})
        app = App.get_running_app()
        self.label.text = f"Vote result: {suspect}\nVotes: {votes}\n"
        if suspect == app.player_id:
            self.label.text += "You were accused!"
        # wait for game_over
        Clock.schedule_once(self.wait_game_over, 2)

    def wait_game_over(self, dt):
        # just wait, server will send game_over
        pass
    
    @mainthread
    def handle_message(self, msg):
        app = App.get_running_app()
        if msg.get("type") == "game_over":
            winner = msg["winner"]
            self.label.text += f"\nGame over! {winner} win!"
            btn = Button(text="Play Again", size_hint=(1, 0.2))
            btn.bind(on_press=lambda x: app.client.send("restart_game"))
            self.layout.add_widget(btn)
    
