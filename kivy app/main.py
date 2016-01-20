# Filename: main.py
import random
import time
import Leaderboard
import multiprocessing
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout



# TO DO LIST:
# Finish leader board pop up & add client server code
# Add images/sprites
# Add time bonus to score
# Make speed relative to window size
# Make truck number relative to window size

INITIAL_RUNTIME = 30
SCORE = 0
TRUCK_NUMBER = 20


class PlayerObject(Widget):
    """ Player controlled object """
    score = NumericProperty(SCORE)

    def truck_collision(self, truck):
        """ The function minuses 1 from the current score value when an instance of Player collides
        with an instance of Trucks
        :param truck: truck is an instance of the Trucks class
        :return:
        """
        if self.collide_widget(truck):
            truck.x -= 500
            self.score -= 1

class Trucks(Widget):
    def choose_color(self):
        truck_colour = random.randint(1,3)
        if truck_colour == 1:
            image_source ="G:\Documents\GitHub\COMP130\comp-130-mobile-game-app\Kivy App\Resources\yellow_truck.png"




    def move(self):
        """ This function adds the value of speed to an instance of Truck's x coordinate every time it's called
        :return:
        """
        if self.center_x > TheGame.width:
            self.center_x = 0
            print TheGame.width
        else:
            self.center_x += self.speed
            print self.speed


class TheGame(Widget):
    player = PlayerObject()
    timer = NumericProperty(INITIAL_RUNTIME)
    level = NumericProperty(1)
    speed = NumericProperty(2)
    width_or_height = "width"
    game_over = "False"

    traffic_list = []

    end = Label()
    help = Button()
    score = Button()

    def get_coordinates(self):
        if self.width_or_height == "width":
            window_dimension = self.width
        elif self.width_or_height == "height":
            window_dimension = self.height - 100
        size = int(window_dimension / 100)
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
        for t in range(TRUCK_NUMBER):
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
        if self.game_over == "False":
            if self.timer <= 0:
                self.end_game()
            else:
                self.timer -= 1
        else:
            self.timer = 0

    def end_game(self):
        """ When called this function removes all the Trucks instances in traffic_list and sets the label
        text to read 'GAME OVER'
        :return:
        """
        for t in self.traffic_list:
            self.remove_widget(t)
        self.end.text = 'GAME OVER'
        self.next_level()

    def help_popup(self):
        popup = Popup(title='Help', content=Label(text='Instructions'), size_hint=(None, None), size=(400, 300))
        popup.open()

    def update(self, dt):
        for t in self.traffic_list:
            if t.center_x > self.width:
                t.center_x = -100
            else:
                t.center_x += self.speed
            self.player.truck_collision(t)
            # t.close_trucks(t)

    def next_level(self):
        if self.level == 1:
            self.level += 1
            self.player.center_y = 0
            self.traffic(self.traffic_list)
            self.speed = 4
            self.end.text = 'Next level!'
            self.timer == 20
        else:
            self.timer == 0
            # Leaderboard.LeaderboardApp()
            # multiprocessing.Process(target=Leaderboard.LeaderboardApp().run).start()
            # Leader board/ server stuff

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
        if self.player.center_y > self.height:
            self.end_game()


class COMP130App(App):
    def build(self):
        game = TheGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.the_timer, 1.0)
        Clock.schedule_once(game.traffic)
        return game


if __name__ == '__main__':
    COMP130App().run()
