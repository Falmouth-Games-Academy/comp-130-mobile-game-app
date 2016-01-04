__author__ = 'Tom'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class snakeGame(Widget):
    pass

class snakeApp(App):
    def build(self):
        return snakeGame()

if __name__ == "__main__":
    snakeApp().run()
