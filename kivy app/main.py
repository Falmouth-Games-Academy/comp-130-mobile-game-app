# Filename: main.py
# Author: 1507866
import random
import time
import Leaderboard
import multiprocessing
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button

INITIAL_RUNTIME = 30
SCORE = 0
TRUCK_NUMBER = 20


class PlayerObject(Widget):
    """ Player controlled object """
    score = NumericProperty(SCORE)
    jump_sound = SoundLoader.load('Resources\jump.wav')

    def truck_collision(self, truck):
        """ The function minuses 1 from the current score value when an instance of Player collides
        with an instance of Trucks
        :param truck: truck is an instance of the Trucks class
        :return:
        """
        if self.collide_widget(truck):
            # If truck and player collide truck is moved off screen
            truck.x -= 500
            self.score -= 1


class Trucks(Widget):
    """ This is the class for the truck object. When an instance of this class is created one of the four coloured
    trucks is randomly chosen and displayed on screen"""
    image_source = StringProperty()

    def __init__(self, **kwargs):
        super(Trucks, self).__init__(**kwargs)
        truck_colours = ["Resources/yellow_truck.png", "Resources/blue_truck.png", "Resources/red_truck.png",
                         "Resources/green_truck.png"]
        self.image_source = random.choice(truck_colours)


class TheGame(Widget):
    player = PlayerObject()
    timer = NumericProperty(INITIAL_RUNTIME)
    level = NumericProperty(1)
    speed = NumericProperty(2)
    width_or_height = "width"  # This variable will be used in the get coordinates

    traffic_list = []

    end = Label()
    help = Button()
    score = Button()

    def help_button(self):
        """ Creates a pop up when called that displays instructions on how to play game."""
        popup = Popup(title='Help', content=Label(text='Instructions'), size_hint=(None, None), size=(400, 300))
        popup.open()

    def get_coordinates(self):
        """ Generates possible X and Y values for trucks based on screen size.
        Returns list of possible X or Y values
        :return: options
        """
        if self.width_or_height == "width":
            self.window_dimension = self.width
        elif self.width_or_height == "height":
            self.window_dimension = self.height - 100
            # the -100 prevents trucks from spawning over the timer/level/score
        size = int(self.window_dimension / 100)
        position = 100
        options = []
        for i in range(size):
            options.append(position)
            position += 100
        return options

    def traffic(self, traffic_list):
        """This function generates instances of the Trucks objects and adds it to traffic_list. Each instance
        has a random X value and a Y value randomly chosen from a list
        :param traffic_list: traffic_list is a list containing all the instances of the Trucks class
        :return:
        """
        for i in range(TRUCK_NUMBER):
            truck = Trucks()
            self.width_or_height = "height"
            y_options = self.get_coordinates()
            y_choice = random.choice(y_options)
            self.width_or_height = "width"
            x_options = self.get_coordinates()
            x_choice = random.choice(x_options)
            truck.center_x = x_choice
            truck.center_y = y_choice
            self.add_widget(truck)
            self.traffic_list.append(truck)
        return self.traffic_list

    def the_timer(self, timer):
        """ This function minus one from the current timer value whenever called.
        :param timer: passes in the current value of timer that's being displayed on screen
        :return:
        """
        if self.timer == 0:
            self.end_game()
            self.timer -= 1
        else:
            self.timer -= 1

    def update(self, dt):
        """ Updates truck positions and check for collisions
        :param dt:
        :return:
        """
        for truck in self.traffic_list:
            if truck.center_x > self.width:
                truck.center_x = -100
            else:
                truck.center_x += self.speed
            self.player.truck_collision(truck)

    def on_touch_move(self, touch):
        """ This function moves the player controlled object when the object is touched """
        # moves player right
        if touch.x > self.player.center_x:
            self.player.center_x += 45
            self.player.jump_sound.play()
            time.sleep(0.1)
        # moves player up
        if touch.y > self.player.y:
            self.player.center_y += 45
            time.sleep(0.1)
            self.player.jump_sound.play()
            self.player.score += 1
        # moves player left
        if touch.x < self.player.center_x:
            self.player.center_x -= 45
            self.player.jump_sound.play()
            time.sleep(0.1)
        # Don't want player to be able to move back

        # prevents player object from leaving the screen
        if self.player.center_y > self.height:
            self.end_game()

    def end_game(self):
        """ When called this function removes all the Trucks instances in traffic_list and sets the label
        text to read 'GAME OVER'
        :return:
        """
        for truck in self.traffic_list:
            self.remove_widget(truck)
        self.end.text = 'GAME OVER'
        self.next_level()

    def next_level(self):
        if self.level == 1:
            self.level += 1
            self.player.center_y = 0
            self.player.center_x = self.width/2
            self.traffic(self.traffic_list)
            self.speed = 4
            self.end.text = 'Next level!'
            self.timer = 20
        else:
            multiprocessing.Process(target=Leaderboard.LeaderBoardApp().run).start()
            # App.get_running_app().screens.current = 'high_score'


class GameScreen(Screen):
    def __init__(self, **kwargs):
        """ Adds an instance of TheGame to a screen to be used by a screen manager"""
        super(GameScreen, self).__init__(**kwargs)
        self.game = TheGame()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        Clock.schedule_interval(self.game.the_timer, 1.0)
        Clock.schedule_once(self.game.traffic)
        self.add_widget(self.game)

"""
class HighScoreScreen(Screen):
    def __init__(self, **kwargs):
        super(HighScoreScreen, self).__init__(**kwargs)
        self.the_layout = Leaderboard.LeaderBoardLayout()
        self.the_layout.create_layout()
        self.add_widget(self.the_layout)"""


class COMP130App(App):
    def build(self):
        self.screens = self.create_screens()
        return self.screens

    def create_screens(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(GameScreen(name='game'))
        # screen_manager.add_widget(HighScoreScreen(name='high_score'))
        return screen_manager


if __name__ == '__main__':
    COMP130App().run()
