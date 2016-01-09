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
    xtouch = NumericProperty(0)
    ytouch = NumericProperty(0)

    def on_touch_down(self, touch):
        #super(Monster, self).on_touch_down(touch)
        xtouch = touch.x
        ytouch = touch.y
        movex = NumericProperty(0)
        movey = NumericProperty(0)
        if xtouch >= self.Monster.center_x:
            movex = movex + 10


        print(xtouch, ytouch)

        Animation.cancel_all(self)
        anim = Animation(x = movex,y = movey , duration = 1, t = 'out_sine')
        print(xtouch,ytouch)
        anim.start(self)
        return anim


snakeGameKivy = Builder.load_file("snake.kv")
class snakeApp(App):
    def build(self):
        game = snakeGameKivy
        return game

if __name__ == "__main__":
    snakeApp().run()
