from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget


class LeaderBoardLayout(Widget):
    def __init__(self, **kwargs):
        super(LeaderBoardLayout, self).__init__(**kwargs)
        self.choice_button = Button(text="Get results")
        self.results_label = Label(text="High scores", font_size='20sp')
        self.name_input = TextInput(text='Enter username here.', multiline=False)
        self.choices_dropdown = DropDown()
        self.dropdown_button = Button(text="Select an option")
        self.dropdown_button.bind(on_release=self.choices_dropdown.open)
        self.layout = GridLayout(rows=5)
        self.drop_down_options = ["Top 10 Scores", "Add New User", "Top scores for user"]
        self.URL_choice = "None"

    def create_layout(self):
        self.choice_button.bind(on_press=self.callback)

        for d in self.drop_down_options:
            btn = Button(text=d, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.choices_dropdown.select(btn.text))
            self.choices_dropdown.add_widget(btn)
        self.choices_dropdown.bind(on_select=lambda instance, x: setattr(self.dropdown_button, 'text', x))

        self.layout.add_widget(self.dropdown_button)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.choice_button)
        self.layout.add_widget(self.results_label)
        return self.layout

    def choice_made(self):
        self.choice_button.text = self.mainbutton.text
        self.layout.add_widget(self.choice_button)

    def got_top_10(self, request, results):
        self.results_label.text = str(results)

    def callback(self, event):
        playername = self.name_input.text[:3]
        self.name_input.text = playername
        self.results_label.text = "Getting scores"

        if self.dropdown_button.text == "Top 10 Scores":
            self.URL_choice = 'http://bsccg04.ga.fal.io/top10.py'
        elif self.dropdown_button.text == "Add New User":
            self.URL_choice = 'http://bsccg04.ga.fal.io/new_user.py?playername=' + playername
        elif self.dropdown_button.text == "Top scores for user":
            self.URL_choice = 'http://bsccg04.ga.fal.io/users_high_score.py?playername=' + playername

        request = UrlRequest(self.URL_choice, self.got_top_10)


class LeaderBoardApp(App):
    def build(self):
        making_layout = LeaderBoardLayout()
        the_layout = making_layout.create_layout()
        return the_layout

LeaderBoardApp().run()
