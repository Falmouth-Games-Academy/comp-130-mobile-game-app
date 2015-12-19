import kivy
kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import random
from kivy.config import Config
# don't make the app re-sizeable
Config.set('graphics', 'resizable', 0)


class TrashCan(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class Cracker(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class TrashGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)

    def serve_ball(self, vel=(0, -4)):
        self.ball.top = self.top + 200
        self.ball.random = self.x
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        # went off a side to score point
        if self.ball.y < self.y-200:
            self.player1.score -= 1
            self.serve_ball(vel=(0, -4))
        if self.ball.collide_widget(self.player1):
            self.player1.score += 1
            self.serve_ball(vel=(0, -4))

    def on_touch_move(self, touch):
        if touch.y < self.width:
            self.player1.center_x = touch.x


     #def update_string(self, req, results):
         #self.hello_world = results

     #def button_pressed(self):
         #req = UrlRequest("http://bsccg06.ga.fal.io/hello_world/?user=Class", self.update_string)


class TrashApp(App):
    def build(self):
        game = TrashGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 0.01 / 60.0)
        return game


if __name__ == '__main__':
    TrashApp().run()
