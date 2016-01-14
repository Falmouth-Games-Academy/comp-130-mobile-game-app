from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Triangle, Line)
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup, Canvas
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.core.audio import SoundLoader, Sound
from kivy.uix.image import Image
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty, ReferenceListProperty,\
ObjectProperty, StringProperty, ListProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.animation import Animation
import math
from random import random
import cgitb
cgitb.enable()



class StartScreen(Screen):
    def on_text(self, username_text):
        print('The widget', self, 'have:', username_text)
        self.username_text = username_text
        return username_text


    textinput = TextInput()
    textinput.bind(text=on_text)


    hello_world = StringProperty()


    def update_string(self, req, results):
        self.hello_world = results


    def username_button_pressed(self):
        username = StringProperty()
        username = self.username_text
        req = UrlRequest("http://bsccg08.ga.fal.io/Input_names/?FirstName=" + username, self.update_string)




class Asteroid_movement(Widget):
    pass


class Boom(Image):
    sound = SoundLoader.load("Sounds\Boom.wav")
    def Boom(self, **kwargs):
        self.__class__.sound.play()
        super(Boom, self).__init__(**kwargs)

class Ammo(Image):

    def shoot(self, tx, ty, target):
        self.target = target
        self.animation = Animation(x=tx, top=ty)
        self.animation.bind(on_start = self.on_start)
        self.animation.bind(on_progress = self.on_progess)
        self.animation.bind(on_complete = self.on_stop)
        self.animation.start(self)


    def on_start(self, instance, value):
        self.boom = Boom()
        self.boom.center = self.center
        self.parent.add_widget(self.boom)

    def on_progress(self, instance, value, progression):
        if progression >= 0.1:
            self.parent.remove_widget(self.boom)
        if self.target.collide_ammo(self):
            self.animation.stop(self)

    def on_stop(self, instance, value):
        self.parent.remove_widget(self)

class Shot(Ammo):
    pass







class Game(Screen, Widget):
    Asteroid = ObjectProperty(None)

    #def serve_ball(self, vel=(4, 0)):
    #    self.ball.center = self.center
    #    self.ball.velocity = vel
    def update(self):
        self.Asteroid.move()

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1





#class controling the movement of the ship
class Ship(Widget):

    xtouch = NumericProperty(0)
    ytouch = NumericProperty(0)
    degrees = NumericProperty(0)

    def on_touch_down(self, touch):

        xtouch = touch.x
        ytouch = touch.y

        Animation.cancel_all(self)
        anim = Animation(x=xtouch, y=ytouch, duration=2.5, t='out_sine')
        anim.start(self)

        #x1,y1 is the ships current position
        #x2,y2 is the postition it is moving to
        x1 = self.x
        y1 = self.y
        x2 = touch.x
        y2 = touch.y


        deltaX = x2 - x1
        deltaY = y2 - y1

        angle = math.atan2(deltaY, deltaX)

        #convert it from 180 degrees to 360
        if (self.degrees <= 0):
            self.degrees = 360 - (-self.degrees)

        #convert it from radians to degrees
        self.degrees = angle * (180 / math.pi)
        #print (self.degrees)



#Gets the highscores from the database
class HighScores(Screen):

    Highscores = StringProperty()
    def update_string(self, req, results):
        self.Highscores = results


    def highscores_button_pressed(self):
        req = UrlRequest("http://bsccg08.ga.fal.io/Highscores/?Highscore=printnames", self.update_string)


#Class used for managing the different screens
class MyScreenManager(ScreenManager):
    pass

HSpresentation = Builder.load_file("HighScores.kv")
Asteroidspresentation = Builder.load_file("Asteroids.kv")

class Asteroids(App):
    def build(self):
        game = Asteroidspresentation
        asteroid = HSpresentation
        #Game.serve_ball()
        #Clock.schedule_interval(Game.update, 1 / 60.0)
        return game








if __name__ == '__main__':
    Asteroids().run()
