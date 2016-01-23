from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import main

Builder.load_string("""

<GameScreen>:
    BoxLayout:
        Button:
            text: 'Play Game'
            on_press: root.run_game()
        Button:
            text: 'Menu'
            on_press: root.manager.current = "game"

""")


class GameScreen(Screen):
    def run_game(self):
        the_game = main.COMP130App()
        the_game.run()


class MenuScreen(Screen):
    pass

screen_manager = ScreenManager()
game = GameScreen(name='game')
screen_manager.add_widget(game)
screen_manager.add_widget(MenuScreen(name='menu'))


class ScreensApp(App):

    def build(self):
        return screen_manager

if __name__ == '__main__':
    ScreensApp().run()
