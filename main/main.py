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
from kivy.core.window import Window
from kivy.uix.button import Button

'''Prevents the user from changing the window size'''
Config.set('graphics', 'resizable', 0)


# setting up the two score counters
class TrashCan(Widget):
    score = NumericProperty(0)
    score_loss = NumericProperty(0)


# setting up the cracker and making it move
class Cracker(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        '''The velocity for the Cracker is set up here'''
        self.pos = Vector(*self.velocity) + self.pos


# class used to get uniform button styles
# NOTE: This peace of code is from the MyButton Class line 30
# Available online at https://kivyspacegame.wordpress.com/
class MyButton(Button):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.font_size = Window.width*0.018


# The main functionality of the game is stored here
class TrashGame(Widget):
    cracker = ObjectProperty(None)
    player = ObjectProperty(None)

    # NOTE: This peace of code is a modified version of the gameOver Definition
    # Line 35 Available online at https://kivyspacegame.wordpress.com/
    def game_over(self):
        '''This is not the parameter for loosing but the action taken
        once that parameter has been met'''
        # add a restart button
        restart_button = MyButton(text='Game Over!!')
        self.add_widget(restart_button)
        restart_button.background_color = (.5, .5, 1, .2)
        self.parent.remove_widget(restart_button)
        # Pause the cracker from spawning
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 1.0/60.0)
        restart_button.size = (Window.width*.3, Window.width*.1)
        restart_button.pos = Window.width*0.5-restart_button.width/2, Window.height*0.53

    def serve_cracker(self):
        '''This serves a cracker each time a point is scored/lost'''
        # these are used to create a random speed of each cracker
        position_x = randint(-15, 15)
        position_y = randint(-18, -16)
        vel = (position_x, position_y)
        # These are used to start the cracker in a random position each time one spawns.
        self.cracker.x = randint(-1, 750)
        self.cracker.y = randint(600, 601)
        self.cracker.velocity = vel

    def serve_another_cracker(self, args):
        '''This will cause the cracker to appear randomly half way down the screen
        to increase difficulty'''
        # these are used to create a random speed of each cracker
        position_x = randint(-15, 15)
        position_y = randint(-18, -16)
        vel = (position_x, position_y)
        # These are used to start the cracker in a random position each time one spawns.
        self.cracker.x = randint(-1, 750)
        self.cracker.y = randint(300, 301)
        self.cracker.velocity = vel

    def update(self, dt):

        self.cracker.move()
        '''bounce cracker off left and right'''
        if (self.cracker.x < 0) or (self.cracker.right > self.width):
            self.cracker.velocity_x *= -1

        '''If you catch the Cracker you score a point, if you miss it you loss a point'''
        if self.cracker.y < self.y-0:
            self.player.score_loss += 1
            self.serve_cracker()
        if self.cracker.collide_widget(self.player):
            self.player.score += 1
            self.serve_cracker()
        '''The loosing condition is set up and the game_over
        function is called when the condition is met'''
        # NOTE: This peace of code below is a modified version of the gameOver parameters
        # Line 83 Available online at https://kivyspacegame.wordpress.com/
        if self.player.score_loss >= 10:
            # game over routine
            self.game_over()
            # Pause the game
            Clock.unschedule(self.update)

    def on_touch_move(self, touch):
        '''Movement for the player'''
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
        # This allows the Cracker to be randomly spawned half way down
        # the screen every 2 seconds
        Clock.schedule_interval(game.serve_another_cracker, 2.0)
        return game


if __name__ == '__main__':
    TrashApp().run()