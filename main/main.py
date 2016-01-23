# Author James Hellman
# Sourcecode from kivy Pong
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.config import Config
from kivy.properties import ListProperty
#from dock import Dock


# don't make the app re-sizeable
Config.set('graphics', 'resizable', 0)


class TrashCan(Widget):
    # setting up the two score counters
    score = NumericProperty(0)
    score_loss = NumericProperty(0)


class Cracker(Widget):
    # setting up the cracker and making it move
    player = ObjectProperty(None)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def redraw(self, args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    # def __init__(self, pos, **kwargs):
    #     super(Cracker, self) .__init__(**kwargs)
    #     self.size = 50, 50
    #     self.pos = pos
    #     with self.canvas:
    #         self.bg_rect = Ellipse(
    #                 source=r"C:\Users\james\Documents\GitHub\comp-130-mobile-game-app\Pictures\cracker-md.png",
    #                 pos=self.pos, size=self.size)
    #     self.bind(pos=self.redraw, size=self.redraw)

    def update_crackers(self):
        pass

        self.pos = Vector(*self.velocity) + self.pos
        '''bounce cracker off left and right'''
        if (self.x < 0) or (self.right > self.width):
            self.velocity_x *= -1

        '''If you catch the Cracker you score a point, if you miss it you loss a point'''
        if self.y < self.y-0:
            self.player.scoreLoss += 1
            # self.serve_cracker()
        #if self.collide_widget(self.player):
            #self.player.score += 1


class TrashGame(Widget):
    crackers = ListProperty([])

    def serve_crackers(self):

        for c in range(0, 6):
            cracker = Cracker()

            pos_x = randint(-1, 200)
            pos_y = randint(10, 500)
            pos = (pos_x, pos_y)
            cracker.pos = pos

            velocity_x = randint(-15, 10)
            velocity_y = randint(-16, -1)
            vel = (velocity_x, velocity_y)
            self.cracker.velocity = vel

            self.crackers.append(cracker)
            self.add_widget(cracker)
            self.bind()

    def clock(self, timer):
        self.timer += 1

    def update(self, dt):
        print len(self.crackers)
        for cracker in self.crackers:
            cracker.update_crackers()
            print (cracker.pos)
            print (cracker.size)
            print self.parent
            print cracker.parent

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
        game.serve_crackers()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    TrashApp().run()
