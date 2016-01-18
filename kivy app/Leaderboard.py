from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest
import cgitb

cgitb.enable()


class LeaderboardApp(App):
    score_button = Button(text="Get scores")
    results_label = Label(text="High scores", font_size='20sp')

    def build(self):
        layout = GridLayout(rows=3)
        self.score_button.bind(on_press=self.callback)
        layout.add_widget(self.score_button)
        layout.add_widget(self.results_label)
        return layout

    def got_weather(self, request, results):
        self.results_label.text = results

    def callback(self, event):
        self.results_label.text = "Getting scores"
        request = UrlRequest('http://bsccg04.ga.fal.io/top10.py', self.got_weather)

# LeaderboardApp().run()
