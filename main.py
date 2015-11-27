from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty, ReferenceListProperty,\
ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
import cgitb
cgitb.enable()





class AsteroidsGame(Widget):

    hello_world = StringProperty()
    def update_string(self, req, results):
        self.hello_world = results


    def button_pressed(self):
        req = UrlRequest("http://bsccg01.ga.fal.io/hello_world/?user=Class", self.update_string)



class AsteroidsApp(App):
    def build(self):
        return AsteroidsGame()





#class Ship(Widget):
 #   velocity_x = numericproperty(0)
 #   velocity_y = numericproperty(0)




if __name__ == '__main__':
    AsteroidsApp().run()
