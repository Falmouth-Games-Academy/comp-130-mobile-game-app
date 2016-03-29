#Below are all of my imports required for work
import kivy
kivy.require('1.7.2')

from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle
import random

from kivy.config import Config

#The code below controlls the window of the game
Config.set('graphics','resizable',1)
Window.clearcolor = (0,255,100,1)
Window.size = (672, 420) #This is the size of the window (X Axis, Y Axis)


class WidgetDrawer(Widget): #This class draws everything on screen
    def __init__(self, imageStr, **kwargs):
        super(WidgetDrawer, self).__init__(**kwargs)
        with self.canvas:
            self.size = (Window.width*.002*25,Window.width*.002*25)
            self.rect_bg=Rectangle(source=imageStr,pos=self.pos,size = self.size)
            self.bind(pos=self.update_graphics_pos)
            self.x = self.center_x #Center X position of the Widget
            self.y = self.center_y #Center Y position of the Widget
            self.pos = (self.x,self.y)
            self.rect_bg.pos = self.pos

    def update_graphics_pos(self, instance, value): #This updates the graphics while movement happens on screen
        self.rect_bg.pos = value
    def setSize(self,width, height): #Updates Size
        self.size = (width, height)
    def setPos(xpos,ypos): #Updates Position
        self.x = xpos
        self.y = ypos

class Sharks(WidgetDrawer): #Declaring the Sharks class

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    #initialize the velocities
    def move(self): #update the position of the Sharks using the velocity.
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y

    def update(self): #the update function moves the surfer.
        self.move()


class Surfer(WidgetDrawer): #Surfer class

    impulse = 2 #moves ship up
    grav = -1 #move ship down

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y

        if self.y >Window.height*0.95: #This is responsible for not letting the surfer go above screen
            self.impulse = -3


    def determineVelocity(self):
        self.grav = self.grav*1.21 #Gravity Intensity
        if self.grav < -6:
            self.grav = -6

        self.velocity_y = self.impulse + self.grav
        self.impulse = 0.95*self.impulse

    def update(self):
        self.determineVelocity()
        self.move()

class MyButton(Button): #Button defined to try again
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.font_size = Window.width*0.018


class GUI(Widget):
    sharkList =[]
    minProb = 1700
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        l = Label(text='Hotel Surfer') #Tile of the game in game
        l.x = Window.width/2 - l.width/2
        l.y = Window.height*0.8
        self.add_widget(l) #adds the label

        self.surfer = Surfer(imageStr = '.\Images\surfer.png')
        self.surfer.x = Window.width/4
        self.surfer.y = Window.height/2
        self.add_widget(self.surfer)

    def addShark(self):
        imageNumber = random.randint(1,4) #This rotates in random between all 4 shark images
        imageStr = './Images/shark_'+str(imageNumber)+'.png' #The image location is defined here
        tmpShark = Sharks(imageStr)
        tmpShark.x = Window.width*1

        #randomizing the Y position
        ypos = random.randint(1,16)

        ypos = ypos*Window.height*.0625

        tmpShark.y = ypos
        tmpShark.velocity_y = 0
        vel = 25
        tmpShark.velocity_x = -0.1*vel

        self.sharkList.append(tmpShark)
        self.add_widget(tmpShark)

    def on_touch_down(self, touch): #Touch controlls for the game
        self.surfer.impulse = 3 #Goes up
        self.surfer.grav = -0.1 #Then applies gravity giving the effect of down

    def gameOver(self):
        restartButton = MyButton(text='Its about ENDURANCE! Try again')
        def restart_button(obj):
            print 'restart button pushed'
            for k in self.sharkList:
                self.remove_widget(k)
                #respawn position x & y for the serfer once the button is pressed.
                self.surfer.xpos = Window.width*0.25
                self.surfer.ypos = Window.height*0.5
                self.minProb = 1700
            self.sharkList = []

            self.parent.remove_widget(restartButton)
            Clock.unschedule(self.update)
            Clock.schedule_interval(self.update, 1.0/60.0)
        restartButton.size = (Window.width*.3,Window.width*.1)
        restartButton.pos = Window.width*0.5-restartButton.width/2, Window.height*0.5
        restartButton.bind(on_release=restart_button)
        self.parent.add_widget(restartButton)

    def update(self, dt):
        self.surfer.update()
        tmpCount = random.randint(1,1800)
        if tmpCount > self.minProb:
            self.addShark()
            if self.minProb < 900:
                self.minProb = 900
            self.minProb = self.minProb +2

        for k in self.sharkList:
            if k.collide_widget(self.surfer):
                print 'death'
                self.gameOver()
                Clock.unschedule(self.update)
            k.update()


class HotelSurferGame(App):

    def build(self):
        parent = Widget()
        app = GUI()
        Clock.schedule_interval(app.update, 1.0/60.0)
        parent.add_widget(app)
        return parent

if __name__ == "__main__":
    HotelSurferGame().run()