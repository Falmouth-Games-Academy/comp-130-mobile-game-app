from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Triangle, Line)
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup, Canvas
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty, ReferenceListProperty,\
ObjectProperty, StringProperty, ListProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.animation import Animation
from random import random
import cgitb
cgitb.enable()



class StartScreen(Screen):



    def on_text(self, username_text):
        print('The widget', self, 'have:', username_text)
        self.username_text = username_text
      #  self.button_pressed.username = username_text

    textinput = TextInput()
    textinput.bind(text=on_text)


    hello_world = StringProperty()


    def update_string(self, req, results):
        self.hello_world = results


    def button_pressed(self):
        username = StringProperty()
        username = self.username_text
        req = UrlRequest("http://bsccg08.ga.fal.io/hello_world/?user=" + username + "." , self.update_string)
  # req = UrlRequest("http://bsccg08.ga.fal.io/hello_world/?user=%s(username)" , self.update_string)



class Asteroid(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class Game(Screen, Widget):
    ball = ObjectProperty(None)


    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1





class Ship(Widget):
    xtouch = NumericProperty(0)
    ytouch = NumericProperty(0)

    def on_touch_down(self, touch):
        xtouch = touch.x
        ytouch = touch.y
        print(xtouch,ytouch)

        Animation.cancel_all(self)
        anim = Animation(x=xtouch, y=ytouch, duration=1, t='out_sine')
        print(xtouch, ytouch)
        anim.start(self)
        return anim







class MyScreenManager(ScreenManager):
    pass



HSpresentation = Builder.load_file("HighScores.kv")
Asteroidspresentation = Builder.load_file("Asteroids.kv")

class Asteroids(App):
    def build(self):
        game = Asteroidspresentation
        asteroid = HSpresentation
        #Game.serve_ball(self)
        #Clock.schedule_interval(Game.update, 1 / 60.0)
        return game








if __name__ == '__main__':
    Asteroids().run()
