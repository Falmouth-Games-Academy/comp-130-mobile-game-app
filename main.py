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
        #username_input.color = colour


    #def on_enter(instance, value):
     #   print('User pressed enter in', instance)

    #textinput = TextInput(text='Hello world', multiline=False)
    #textinput.bind(on_text_validate=on_enter)
        #textinput = TextInput(text='Hello world')

        #self.cols = 4
        #self.rows = 2
        #self.add_widget(Label(text="Username:"))
        #self.username = TextInput(multiline=False)
        #self.add_widget(self.username)

        #self.add_widget(Label(text="Password:: ") )
        #self.password = TextInput(multiline=False, password=True)
        #self.add_widget(self.password)

        #self.add_widget(Button(text="Button"))
        #self.button = Button(background_color=[1,1,1,1])
        #self.add_widget(self.button)



    hello_world = StringProperty()

    def update_string(self, req, results):
        self.hello_world = results


    def button_pressed(self):
        username = StringProperty()
        username = "Alli"
        print(username)
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
