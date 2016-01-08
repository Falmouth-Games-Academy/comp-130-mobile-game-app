# Filename: menu.py
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from random import randrange, choice


class MenuApp(App):

    def build(self):
        layout = GridLayout(rows=4)
        layout.add_widget(Label(text='Menu', font_size='120sp'))
        layout.add_widget(Button(text='Play Game'))
        layout.add_widget(Button(text='Leaderboard'))
        return layout

MenuApp().run()
