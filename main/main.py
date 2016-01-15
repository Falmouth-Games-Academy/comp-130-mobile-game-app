# Author James Hellman
# Sourcecode from kivy Pong
import kivy
kivy.require('1.0.9')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.config import Config

# don't make the app re-sizeable
Config.set('graphics', 'resizable', 0)


class TrashCan(Widget):
    # setting up the two score counters
    score = NumericProperty(0)
    scoreLoss = NumericProperty(0)


class Cracker(Widget):
    # setting up the cracker and making it move
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class TrashGame(Widget):
    cracker = ObjectProperty(None)
    # player1 and player are used to separate the Caught/Lost scores
    player1 = ObjectProperty(None)
    player = ObjectProperty(None)

# Possibility for adding crackers
#    def add_cracker(self, vel):
#        X = randint(-1, 750)
#        Y = randint(500, 701)
#        self.cracker.velocity = vel
#        self.add_widget(Cracker(vel, pos=(X, Y)))

    def serve_cracker(self, vel=(5, -10)):
        # These are used to start the cracker in a random position each time one spawns.
        self.cracker.x = randint(-1, 750)
        self.cracker.y = randint(600, 601)
        self.cracker.velocity = vel
        # trying to add widgets that move
        # cant figure out how to count the quantity of them on the screen so i can limit them.
        X = randint(-1, 750)
        Y = randint(500, 700)
        self.add_widget(Cracker(vel, pos=(X, Y)))

    def update(self, dt):
        self.cracker.move()
        # these are used to create a random speed of each cracker
        X = randint(-15, 15)
        Y = randint(-15, -6)
        # bounce cracker off left and right
        if (self.cracker.x < 0) or (self.cracker.right > self.width):
            self.cracker.velocity_x *= -1

        # If you catch the Cracker you score a point, if you miss it you loss a point.
        if self.cracker.y < self.y-200:
            self.player1.scoreLoss += 1
            self.serve_cracker(vel=(X, Y))
            self.serve_cracker(vel=(X, Y))
        if self.cracker.collide_widget(self.player1):
            self.player1.score += 1
            self.serve_cracker(vel=(X, Y))
            self.serve_cracker(vel=(X, Y))

    def on_touch_move(self, touch):
        # Movement for the player
        if touch.y < self.width:
            self.player1.center_x = touch.x

# To be used later
# class Online(Widget):

    # def update_string(self, req, results):
        # self.hello_world = results

    # def button_pressed(self):
        # req = UrlRequest("http://bsccg06.ga.fal.io/hello_world/?user=Class", self.update_string)

class TrashApp(App):
    def build(self):
        game = TrashGame()
        game.serve_cracker()
        Cracker()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    TrashApp().run()
