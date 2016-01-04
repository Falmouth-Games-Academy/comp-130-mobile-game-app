from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.image import Image
from kivy.clock import Clock
import random
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Declaring screens for use in screen manager
class BattleScreen(Screen):
    def check_for_monster(self):
        try:
            return self.monster
        except:
            self.monster = self.random_stats()
            return self.monster

    def check_for_player(self):
        try:
            return self.player
        except:
            self.player = self.random_stats()
            return self.player

    def make_stat_text(self, title):                                        # title changes who's stats are displayed
        if title == 'Monster:':
            character = self.check_for_monster()
        elif title == 'Player:':
            character = self.check_for_player()
        else:
            character = self.random_stats()
        for stat in range(0, len(character)):
            title = title + '\n\n' + str(character[stat][0]) + ' = ' + str(character[stat][1])
        return title

    def random_stats(self):
        hp = random.randint(14, 22)
        strength = random.randint(1, 10)
        if strength >= 5:
            dexterity = random.randint(1, int(10 - (strength/4)))
        else:
            dexterity = random.randint(1, int(10 + (strength/4)))
        will = random.randint(1, 10)
        damageResistance = random.randint(0, 5)
        character = []
        character.append(('HP', hp))
        character.append(('Strength', strength))
        character.append(('Dexterity', dexterity))
        character.append(('Will', will))
        character.append(('Toughness', damageResistance))
        character = character
        return character

class MenuScreen(Screen):
    pass

# The application class
class MainApp(App):
    def build(self):
        self.load_sounds()
        self.text = 'here is some\nlovely text'
        return self.load_screens()

    # This function loads screens from the kv file
    def load_screens(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(BattleScreen(name='battle'))
        return sm

    def load_sounds(self):
        self.sounds = {}
        fname = 'sound3.wav'
        self.sounds[0] = SoundLoader.load(fname)

    def play_sound1(self):
        sound = self.sounds.get(0)
        if sound is not None:
            sound.volume = 0.5
            sound.play()

if __name__ == '__main__':
    MainApp().run()
