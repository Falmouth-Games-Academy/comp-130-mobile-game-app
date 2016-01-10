# Filename: main.py
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import time
from random import randrange, choice


popup = Popup(title='Welcome', content=Label(text='Instructions'), size_hint=(None, None), size=(400, 300))


class PlayerObject(Widget):
    score = NumericProperty(0)
    lives = NumericProperty(3)


class Trucks(Widget):
    def __init__(self):
        y_options = [100, 200, 300, 400]
        y_coord = random.choice(y_options)



class TheGame(Widget):
    layout = BoxLayout
    layout.add_widget(PlayerObject)


class COMP130App(App):
    def build(self):
        popup.open()
        game = TheGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    COMP130App().run()
