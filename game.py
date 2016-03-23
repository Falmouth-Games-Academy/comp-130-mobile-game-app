from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button
import sys






class PongPaddle(Widget):
    insectLives = NumericProperty(20)
    lives = NumericProperty(3)
    def bounce_ball(self, ball):

        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.2
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    #velocity x is horizontal speed.
    velocity_x = NumericProperty(0)
    #vlocity y is vertical speed.
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player2 = ObjectProperty(None)
    #This is how the ball resets and serves the ball after.
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        #bounce of puppet
        self.player2.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        #went of to a bounces back left side
        if (self.ball.x < self.x) or (self.ball.width > self.width):
            self.ball.velocity_x *= -1
            self.player1.insectLives -= 1


        #if the player misses the ball he will lose a life and it will serve the ball
        if self.ball.x > self.width:
            self.player2.lives -= 1
            self.serve_ball(vel=(+4, 0))
        #Ends game by putting the ball stationary when the player loses all their lives
        if self.player2.lives == 0 :
            self.serve_ball(vel=(+0, 0))
        #Ends game by putting the ball stationary when the player hits the left side 20 times.
        if self.player1.insectLives == 0 :
            self.serve_ball(vel=(+0, 0))



    def on_touch_move(self, touch):
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y




class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()