import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from network import GameClient
from screens.main_menu import MainMenu
from screens.lobby import Lobby
from screens.role_reveal import RoleReveal
from screens.game import Game
from screens.voting import Voting
from screens.result import Result
from utils.constants import SERVER_URL
from os import system
system("cls")
class SpyfallApp(App):
    def build(self):
        self.player_id = ""
        self.room_code = ""
        self.players = []
        self.my_role = ""
        self.location = None
        self.vote_result = None

        self.client = GameClient()
        self.client.connect(SERVER_URL)

        self.sm = ScreenManager()
        self.sm.add_widget(MainMenu(name="main_menu"))
        self.sm.add_widget(Lobby(name="lobby"))
        self.sm.add_widget(RoleReveal(name="role_reveal"))
        self.sm.add_widget(Game(name="game"))
        self.sm.add_widget(Voting(name="voting"))
        self.sm.add_widget(Result(name="result"))
        self.sm.current = "main_menu"
        return self.sm
if __name__ == '__main__':
    SpyfallApp().run()
