# Filename: hello.py
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')

import time
from random import randrange, choice
"""Adapted from the kivy pong tutorial. The pong paddle is now the object controlled by the player.
   The pong ball will be duplicated and become the trucks."""


popup = Popup(title='Welcome',
    content=Label(text='Instructions'),
    size_hint=(None, None), size=(400, 400))
root = Widget()


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    """
    def create_trucks(self):
    global trucks_array   # The variable stars is global so it can be used in other functions
    truck_number = 10
    stars_array = []
    for i in range(truck_number):
        # each star has an x coordinate, a y coordinate and a speed
        star = [randrange(0, width - 1), randrange(0, screen.get_height() - 1), choice([1, 2, 3])]
        stars_array.append(star)
"""


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    #player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        #self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        # if (self.ball.y < self.y) or (self.ball.top > self.top):
          #  self.ball.velocity_y *= -1

        """#went of to a side to score point?
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))"""

    def on_touch_move(self, touch):
        """ This function movies the player controlled object when the object is touched """
        # moves player right
        if touch.x > self.player1.center_x:
            self.player1.center_x += 55
            time.sleep(0.1)
        # moves player up
        if touch.y > self.player1.y:
            self.player1.center_y += 55
            time.sleep(0.1)
            self.player1.score += 1
        # moves player left
        if touch.x < self.player1.center_x:
            self.player1.center_x -= 55
            time.sleep(0.1)
        # Don't want player to be able to move back

        # prevents player object from leaving the screen
        if self.player1.center_y > root.height:
            self.player1.score += 100
            # End game when player reaches top
            # Use another page for leader board


class COMP130App(App):
    def build(self):
        popup.open()
        game = PongGame()
        # game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    COMP130App().run()
