# Author James Hellman
# Sourcecode from kivy Pong
import kivy
import datetime
kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
# don't make the app re-sizeable
Config.set('graphics', 'resizable', 0)


class TrashCan(Widget):
    score = NumericProperty(0)
    scoreloss = NumericProperty(0)


class Cracker(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def progress(self):
        addwidget


class TrashGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player = ObjectProperty(None)

    def serve_ball(self, vel=(5, -10)):
        self.ball.x = randint(-1, 750)
        self.ball.y = randint(700, 701)
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()
        X = randint(-15, 15)
        Y = randint(-15, -6)
        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        # went off a side to score point
        if self.ball.y < self.y-200:
            self.player1.scoreloss += 1
            self.serve_ball(vel=(X, Y))
        if self.ball.collide_widget(self.player1):
            self.player1.score += 1
            self.serve_ball(vel=(X, Y))

    def on_touch_move(self, touch):
        if touch.y < self.width:
            self.player1.center_x = touch.x

#####TO DO LATER####

#class Online(Widget):

    #def update_string(self, req, results):
       # self.hello_world = results

  #  def button_pressed(self):
     #   req = UrlRequest("http://bsccg06.ga.fal.io/hello_world/?user=Class", self.update_string)


#class Time(Widget):

    #def time(self):
       # self.modes = (
            #'%I:%m:%S',
           # '%H:%m:%S %P',
           # '%S:',
        #)
       # self.mode = 0
       # self.main_box = BoxLayout(orientation='vertical')

       # self.button = Button(text='label', font_size=100, font_name='comic.ttf')
       # self.main_box.add_widget(self.button)

       # self.button.bind(on_press=self.tap)
       # Clock.schedule_interval(self.timer, 0.01)

       # return self.main_box

    #def tap(self, button):
        #if self.mode +1 == len(self.modes):
            #self.mode = 0
        #else:
           # self.mode +=1

    #def timer(self, dt):
       # now = datetime.datetime.now()
        #self.button.text = now.strftime(self.modes[self.mode])
        #if self.mode == 2:
            #self.button.text += str(now.microsecond)[:3]


######
class TrashApp(App):
    def build(self):
        game = TrashGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    TrashApp().run()
