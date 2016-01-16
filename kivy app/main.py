# Filename: main.py
import random
import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest

import cgitb
cgitb.enable()
import Leaderboard

# TO DO LIST:
# Finish leader board pop up & add client server code
# Add images/sprites
# Add time bonus to score
# Make speed relative to window size
# Make truck number relative to window size

INITIAL_RUNTIME = 30
LIVES = 3
SCORE = 0
TRUCK_NUMBER = 20


class PlayerObject(Widget):
    """ Player controlled object """
    score = NumericProperty(SCORE)
    lives = NumericProperty(LIVES)

    def truck_collision(self, truck):
        """ The function minuses 1 from the current lives value when an instance of Player collides
        with an instance of Trucks
        :param truck:
        :return:
        """
        if self.collide_widget(truck):
            truck.x = -750
            if self.lives > 0:
                self.lives -= 1
            elif self.lives <= 0:
                print "Game Over"
                # TheGame.end_game()
                # calling end_game() crashes the program
                # Might get rid of lives and just take points of score


class Trucks(Widget):
    def move(self):
        """ This function adds the value of speed to an instance of Truck's x coordinate every time it's called
        :return:
        """
        if self.center_x > TheGame.width:
            self.center_x = 0
        else:
            self.center_x += self.speed

    def close_trucks(self, truck):
        if self.collide_widget(truck):
            truck.x = -50


class TheGame(Widget):
    player = PlayerObject()
    timer = NumericProperty(INITIAL_RUNTIME)
    level = NumericProperty(1)
    speed = NumericProperty(2)

    traffic_list = []

    end = Label()
    help = Button()
    score = Button()

    def traffic(self, traffic_list):
        """This function generates instances of the Trucks objects and adds it to traffic_list. Each instance
        has a random X value and a Y value randomly chosen from a list
        :param traffic_list:
        :return:
        """
        for t in range(TRUCK_NUMBER):
            truck = Trucks()
            y_options = [100, 200, 300, 400, 500]
            y_choice = random.choice(y_options)
            truck.center_x = random.randint(-self.width/2, self.width)
            truck.center_y = y_choice
            self.add_widget(truck)
            self.traffic_list.append(truck)
        return self.traffic_list

    def the_timer(self, timer):
        """ This function minus one from the current timer value whenever called.
        :param timer:
        :return:
        """
        self.timer -= 1

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

    def score_board(self):
        popup = Popup(title='High Scores', content=Label(text='scores'), size_hint=(None, None), size=(400, 300))
        popup.open()
        # doesn't work yet

    def update(self, dt):
        for t in self.traffic_list:
            if t.center_x > self.width:
                t.center_x = 0
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
            print "end"
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
            # end_game()
            # crashes game
            # End game when player reaches top


class COMP130App(App):
    def build(self):
        game = TheGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.the_timer, 1.0)
        Clock.schedule_once(game.traffic)
        return game


if __name__ == '__main__':
    COMP130App().run()
