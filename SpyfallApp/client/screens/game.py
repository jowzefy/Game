from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock
from kivy.clock import mainthread


class Game(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)

        self.log = ScrollView(size_hint=(1, 0.6))
        self.log_label = Label(text="", size_hint_y=None, valign="top")
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        self.log.add_widget(self.log_label)
        main_layout.add_widget(self.log)

        input_layout = BoxLayout(size_hint=(1, 0.2), spacing=5)
        self.msg_input = TextInput(hint_text="Ask a question...", multiline=False)
        input_layout.add_widget(self.msg_input)
        send_btn = Button(text="Send", size_hint_x=0.2)
        send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(send_btn)
        main_layout.add_widget(input_layout)

        btn_vote = Button(text="Vote for Spy", size_hint=(1, 0.15))
        btn_vote.bind(on_press=self.go_to_vote)
        main_layout.add_widget(btn_vote)

        self.add_widget(main_layout)

    def on_enter(self):
        app = App.get_running_app()
        app.client.callback = self.handle_message
        self.log_label.text = ""

    def send_message(self, instance):
        text = self.msg_input.text.strip()
        if text:
            app = App.get_running_app()
            app.client.send("ask_question", {"question": text})
            self.msg_input.text = ""

    def go_to_vote(self, instance):
        app = App.get_running_app()
        app.sm.current = "voting"
    @mainthread
    def handle_message(self, msg):
        app = App.get_running_app()
        msg_type = msg.get("type")
        if msg_type == "question_asked":
            self.log_label.text += f"\n{msg['from']} asks: {msg['question']}"
        elif msg_type == "answer_given":
            self.log_label.text += f"\n{msg['from']} answers: {msg['answer']}"
        
