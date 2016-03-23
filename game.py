from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
import sys
import random





#declaring the pong paddle class
class PongPaddle(Widget):

    insectLives = NumericProperty(20) #Set the lives of the insects to x number
    lives = NumericProperty(3) #Set the lives of the player to x number

    def bounce_ball(self, ball):

        if self.collide_widget(ball):#if the ball colides with the pong paddle then bounce back with increased speed,if it hits the top or bottom change angle of rebound.
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.2
            ball.velocity = vel.x, vel.y + offset



#declaring the pong ball class
class PongBall(Widget):
    #velocity x is horizontal speed.
    velocity_x = NumericProperty(0)
    #vlocity y is vertical speed.
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos



#declaring the Bees class
class Bees(Widget):#setting velocity variables for Bees
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def bmove(self):
        self.pos = Vector(*self.velocity) + self.pos



#declaring the end of game button
class endGameButton(Button):
    def __init__(self, **kwargs):
        super(endGameButton,self).__init__(**kwargs)
        self.font_size = Window.width*0.2




#declaring the pong game class
class PongGame(Widget):
    randprob = 1700 #setting the random probability to 1700
    ball = ObjectProperty(None)
    player2 = ObjectProperty(None)
    bee = ObjectProperty(None)


    #This is how the ball resets and serves the ball after.
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center#serves ball from center.
        self.ball.velocity = vel

    def serve_bee(self,vel=(3,0)):
        self.ball.center = self.center#serves bee from left
        self.ball.velocity = vel



    #def add_Bee(self): #Adding bees in while the game is running
#
 #       tempBee = Bees
  #      posY = random.randint(1,14)
   #     posY = posY*Window.height*.0625
#
 #       tempBee.y = posY
  #      tempBee.velocity_y = 0
   #     tempBee.velocity_x = 20



    #Defineing the gameover and how the button appears and what happens when pressed
    def gameOver(self):
        restart = endGameButton(text='You lose, Try again?') #brings up the endGameButton with text saying retry
        def restartButton(obj):
            print 'Trying again'
        endGameButton.size = (Window.width*.3,Window.width*.1)





    def update(self, dt):
        self.ball.move()

       # simonSays = random.randint(1,1800)
        #if simonSays > self.randprob:
         #   self.add_Bee()
          #  if self.randprob <900:
           #         self.randprob=900
            #self.randprob = self.randprob +2

        #bounce of puppet
        self.player2.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
            self.ball.velocity_y *= -1

        #went of to a bounces back left side
        if (self.ball.x < self.x) or (self.ball.width > self.width):
            self.ball.velocity_x *= -1
            self.player1.insectLives -= 1


        #if the player misses the ball he will lose a life and it will serve the ball----losing lifes
        if self.ball.x > self.width:
            self.player2.lives -= 1
            self.serve_ball(vel=(+4, 0))
        #Ends game by putting the ball stationary when the player loses all their lives----loses all player lifes
        if self.player2.lives == 0 :
            self.gameOver()
            self.serve_ball(vel=(+0, 0))

        #Ends game by putting the ball stationary when the player hits the left side 20 times.----wins the game
        if self.player1.insectLives == 0 :
            self.serve_ball(vel=(+0, 0))



    def on_touch_move(self, touch):
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y




class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        game.serve_bee()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()