from kivy.app import App
from kivy.uix.widget import Widget


class AsteroidsGame(Widget):
    pass


class AsteroidsApp(App):
    def build(self):
        return AsteroidsGame()


if __name__ == '__main__':
    PongApp().run()