# Filename: main.py
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import time
from random import randrange, choice
import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')  # Fixed window size for now

# TO DO LIST:
# If not using pages then menu screens/high score widgets
# Placing trucks generated in array on screen
# Add images/sprites
# Change truck speeds
# Leader board client server code
# Add comments
# End game function - End game when timer or lives = 0

RUNTIME = 30
LIVES = 3
SCORE = 0
TRUCK_NUMBER = 3


popup = Popup(title='Welcome', content=Label(text='Instructions'), size_hint=(None, None), size=(400, 300))


class PlayerObject(Widget):
    """ PLayer controlled object
    """
    score = NumericProperty(SCORE)
    lives = NumericProperty(LIVES)

    def truck_collision(self, truck):
        if self.collide_widget(truck):
            if self.lives > 0:
                self.lives -= 1
            elif self.lives <= 0:
                self.lives = 123


class Trucks(Widget):
    y_options = [100, 150, 200, 300, 400, 500]
    y_choice = random.choice(y_options)

    def move(self):
        if self.center_x > 480:
            self.center_x = 0
        else:
            self.center_x += 5


class RunTime(Widget):
    def the_timer(self, timer):
        self.timer -= 1


class Road(Widget):
    traffic = ListProperty(())
    layout = GridLayout(rows=5)

    def __init__(self, **kwargs):
        super(Road, self).__init__(**kwargs)
        for t in range(0, 3):
            self.add_widget(Trucks)
            self.traffic.append(Trucks)
            print (t)


class TheGame(Widget):
    truck = ObjectProperty(None)
    #truck = Road()
    player = ObjectProperty(None)
    timer = NumericProperty(RUNTIME)
    #road = Road()

    #def __init__(self):
    #   road = Road()
    #   self.add_widget(road)

    def the_timer(self, timer):
        self.timer -= 1

    def update(self, dt):
        self.truck.move()
        # bounce off paddles
        self.player.truck_collision(self.truck)

    def end_game(self):
        popup.open()

    def on_touch_move(self, touch):
        """ This function moves the player controlled object when the object is touched """
        # moves player right
        if touch.x > self.player.center_x:
            self.player.center_x += 45
            time.sleep(0.1)
        # moves player up
        if touch.y > self.player.y:
            self.player.center_y += 45
            time.sleep(0.1)
            self.player.score += 1
        # moves player left
        if touch.x < self.player.center_x:
            self.player.center_x -= 45
            time.sleep(0.1)
        # Don't want player to be able to move back

        # prevents player object from leaving the screen
        if self.player.center_y > 640:
            self.player.score += 100
            #TheGame.end_game()
            # crashes game

            # End game when player reaches top
            # Use another page for leader board


class COMP130App(App):
    def build(self):
        game = TheGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.the_timer, 1.0)
        popup.open()
        return game


if __name__ == '__main__':
    COMP130App().run()
