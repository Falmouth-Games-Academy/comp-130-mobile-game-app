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
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty, ReferenceListProperty,\
ObjectProperty, StringProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
import random
import cgitb
cgitb.enable()




class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        colour = [random.random() for i in range(3)] + [1]

    #username_input = self.ids.username_input
    #username_input.text = "text"


    # def on_enter(instance, value):
    #     print('User pressed enter in', instance, value)
    #
    # textinput = TextInput(text='name')
    # textinput.bind(on_text_validate=on_enter)
    value = StringProperty()


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

class Game(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass



HSpresentation = Builder.load_file("HighScores.kv")
Asteroidspresentation = Builder.load_file("Asteroids.kv")

class Asteroids(App):
    def build(self):
        return Asteroidspresentation








if __name__ == '__main__':
    Asteroids().run()
