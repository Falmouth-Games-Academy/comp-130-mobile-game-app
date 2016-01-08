__author__ = 'Tom'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.animation import Animation


class Menu(Screen):
    pass

class snakeGame(Screen,Widget):
    pass

class HighScoreMenu(Screen):
    pass

class TheScreenManager(ScreenManager):
    pass

class Monster(Widget):
    def on_touch_down(self, touch):
        super(Monster, self).on_touch_down(touch)

snakeGameKivy = Builder.load_file("snake.kv")
class snakeApp(App):
    def build(self):
        game = snakeGameKivy
        return game

if __name__ == "__main__":
    snakeApp().run()
