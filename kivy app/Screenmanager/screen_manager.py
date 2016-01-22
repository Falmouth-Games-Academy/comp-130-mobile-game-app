from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import main
import Leaderboard


class MenuScreen(Screen):
    btn1 = Button()


class PlayGameScreen(Screen):
    main.COMP130App().run()
    


class SettingsScreen(Screen):
    # Leaderboard.LeaderboardApp().run()
    pass
# Create the screen manager
screens = ScreenManager()
screens.add_widget(MenuScreen(name='menu'))
#screens.add_widget(PlayGameScreen(name='game'))


class SceensApp(App):

    def build(self):
        return screens

if __name__ == '__main__':
    SceensApp().run()