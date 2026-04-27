from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock

class RoleReveal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.role_label = Label(font_size=30)
        self.location_label = Label(font_size=24)
        self.layout.add_widget(self.role_label)
        self.layout.add_widget(self.location_label)
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        self.role_label.text = f"Your role: {app.my_role}"
        if app.location:
            self.location_label.text = f"Location: {app.location}"
        else:
            self.location_label.text = "You are the spy! Learn the location."
        # Auto move to game screen after few seconds
        Clock.schedule_once(self.go_to_game, 4)
        # Also allow manual continue
        btn = Button(text="Continue", size_hint=(1, 0.2))
        btn.bind(on_press=lambda x: self.go_to_game(0))
        if not hasattr(self, 'continue_added'):
            self.layout.add_widget(btn)
            self.continue_added = True

    def go_to_game(self, dt):
        app = App.get_running_app()
        app.sm.current = "game"
