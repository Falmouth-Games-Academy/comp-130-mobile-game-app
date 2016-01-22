# Author James Hellman
# Sourcecode from kivy Pong
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
    player = ObjectProperty(None)

    def serve_cracker(self):
        # these are used to create a random speed of each cracker
        X = randint(-15, 15)
        Y = randint(-15, -6)
        vel = (X, Y)
        # These are used to start the cracker in a random position each time one spawns.
        self.cracker.x = randint(-1, 750)
        self.cracker.y = randint(600, 601)
        self.cracker.velocity = vel
        ''' trying to add widgets that move
            cant figure out how to count the quantity of them on the screen so i can limit them'''

    def another_cracker(self, vel):
        self.cracker.x = randint(-1, 750)
        self.cracker.y = randint(600, 601)
        self.cracker.velocity = vel

    def clock(self, timer):
        self.timer += 1

    def update(self, dt):
        self.cracker.move()
        '''bounce cracker off left and right'''
        if (self.cracker.x < 0) or (self.cracker.right > self.width):
            self.cracker.velocity_x *= -1

        '''If you catch the Cracker you score a point, if you miss it you loss a point'''
        if self.cracker.y < self.y-0:
            self.player.scoreLoss += 1
            self.serve_cracker()
        if self.cracker.collide_widget(self.player):
            self.player.score += 1
            self.serve_cracker()

    def on_touch_move(self, touch):
        # Movement for the player
        if touch.y < self.width:
            self.player.center_x = touch.x


# To be used later
#class Online(Widget):

     #def update_string(self, req, results):
        # self.hello_world = results

     #def button_pressed(self):
         #req = UrlRequest("http://bsccg06.ga.fal.io/hello_world/?user=Class", self.update_string)

class TrashApp(App):
    def build(self):
        game = TrashGame()
        game.serve_cracker()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    TrashApp().run()
