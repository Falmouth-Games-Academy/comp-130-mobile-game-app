# Filename: main.py
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import time
from random import randrange, choice
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')  # Fixed window size for now

# TO DO LIST:
# Looking into using Kivy pages or screens (high score page, running page?)
# If not using pages then menu screens/high score widgets
# Placing trucks generated in array on screen
# Add images/sprites
# Change truck speeds
# Leader board client server code
# Add comments
# End game function
# Add timer, score change based on time taken

popup = Popup(title='Welcome', content=Label(text='Instructions'), size_hint=(None, None), size=(400, 400))
root = Widget()
# Try and use pages have start page, a running page and a high score page


class PlayerObject(Widget):
    """ Planning to move PlayerObject into another file and import    """
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            popup.open()
            """vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset"""


class Trucks(Widget):
    # velocity_x = NumericProperty(0)
    # velocity_y = NumericProperty(0)
    # velocity = ReferenceListProperty(velocity_x, velocity_y)

    def create_trucks(self):    #Might move into TheGame and generate instances of Trucks
        truck_number = 10
        global trucks_array
        trucks_array = []
        for i in range(truck_number):
            # Each truck has an X coord, a Y coord and will add speed
            truck = [randrange(0, TheGame.width), randrange(0, TheGame.height)]
            print TheGame.width
            trucks_array.append(truck)

    def move(self):
        if self.center_x > 480:
            self.center_x = 0
        else:
            self.center_x += 5


class TheGame(Widget):
    the_truck = ObjectProperty(None)
    player1 = ObjectProperty(None)
    timer = ObjectProperty(None)

    """def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel"""

    def update(self, dt):
        self.ball.move()
        # bounce off paddles
        self.player1.bounce_ball(self.ball)

    def end_game(self):
        print "END"
        # go back to leader board page

    def on_touch_move(self, touch):
        """ This function moves the player controlled object when the object is touched """
        # moves player right
        if touch.x > self.player1.center_x:
            self.player1.center_x += 45
            time.sleep(0.1)
        # moves player up
        if touch.y > self.player1.y:
            self.player1.center_y += 45
            time.sleep(0.1)
            self.player1.score += 1
        # moves player left
        if touch.x < self.player1.center_x:
            self.player1.center_x -= 45
            time.sleep(0.1)
        # Don't want player to be able to move back

        # prevents player object from leaving the screen
        if self.player1.center_y > 640:
            self.player1.score += 100
            # end_game()
            # gives an error not sure why

            # End game when player reaches top
            # Use another page for leader board


class COMP130App(App):
    def build(self):
        popup.open()
        game = TheGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    COMP130App().run()
