__author__ = 'Tom'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty,StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.network.urlrequest import UrlRequest


class Menu(Screen):

    snakeplayer = StringProperty()

    def update_string(self, req,results):
        self.snakeplayer = results

    def button_press(self):
        user_name = StringProperty()
        req = UrlRequest("http://bsccg07.ga.fal.io/SnakePlayers/?Name=tom", self.update_string)



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
        xtouch = touch.x
        ytouch = touch.y
        movex = self.center_x
        movey = self.center_y
        if xtouch >= self.center_x:
            movex = 50
        else:
            movex = -50
        if ytouch >= self.center_y:
            movey = 50
        else:
            movey = -50

        Animation.cancel_all(self)
        anim = Animation(x = self.x + movex,y = self.y + movey, duration = 0.5)
        anim.start(self)
        return anim


class Trash(Widget):
    pass


snakeGameKivy = Builder.load_file("snake.kv")
class snakeApp(App):
    def build(self):
        game = snakeGameKivy
        return game

if __name__ == "__main__":
    snakeApp().run()
