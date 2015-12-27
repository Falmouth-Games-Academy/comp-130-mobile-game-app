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





class Game(Screen, Widget):
    pass

class Asteroid(Widget):
    #velocity = ListProperty([1,1])

    # def __init__(self, **kwargs):
    #     super(Asteroid, self).__init__(**kwargs)
    #     Clock.schedule_interval(self.anim_to_pos, 1/60.)
    #
    #
    # def update(self, *args):
    #     pass

    #
    #     self.x += self.velocity[0]
    #     self.y += self.velocity[1]
    #
    #
    #     if self.x < (self.x + self.width) > Window.width:
    #         self.velocity[0] *= -1
    #     if self.y < (self.x + self.height) > Window.height:
    #         self.velocity[1] *= -1
    #
    x_touch = 1
    y_touch = 1


    def anim_to_pos(self, xtouch, ytouch):
        Animation.cancel_all(self)
        random_x = random() * (Window.width - 100)
        random_y = random() * (Window.height - 100)

        #print(random_x, random_y, Window.width - self.width)

        anim = Animation(x=xtouch, y=ytouch, duration=1, t='out_elastic')
        print(self.x_touch, self.y_touch)
        anim.start(self)




    def on_touch_down(self, touch):
        self.x_touch, self.y_touch = touch.pos
        xtouch = self.x_touch
        ytouch = self.y_touch

        #
        # with self.canvas:
        #     touch.ud["Rectangle"] = Rectangle(pos=(touch.x, touch.y))
        #


        if self.collide_point(*touch.pos):
            self.anim_to_pos(xtouch, ytouch)









class MyScreenManager(ScreenManager):
    pass



HSpresentation = Builder.load_file("HighScores.kv")
Asteroidspresentation = Builder.load_file("Asteroids.kv")

class Asteroids(App):
    def build(self):
        return Asteroidspresentation








if __name__ == '__main__':
    Asteroids().run()
