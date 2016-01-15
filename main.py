import random
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Declaring screens for use in screen manager
class BattleScreen(Screen):
    pass
#    playerDescription = StringProperty()
#
 #   def update_descriptions(self, playerDesc, monsterDesc):
  #      self.playerDescription.text = playerDesc
   #     self.monsterDescription.text = monsterDesc


class MenuScreen(Screen):
    pass


class LogInScreen(Screen):
    pass


class MainApp(App):
    def build(self):
        self.load_sounds()
        self.generate_player()
        self.playerDescription = StringProperty()
        self.playerDescription = self.get_player_stats()
        self.generate_monster()
        self.monsterDescription = StringProperty()
        self.monsterDescription = self.get_monster_stats()
        return self.load_screens()
# player and monster generation and modification

    def attack_monster(self):
        damage = self.generate_player_damage()
        stat = self.monster[self.find_stat(self.monster, 'Hit Points')][1]
        self.monster[self.find_stat(self.monster, 'Hit Points')][1] = stat - damage
        self.end_turn()

    def end_turn(self):
        self.monsterDescription = self.get_monster_stats
        print self.monsterDescription
        print self.monster

    def generate_player_damage(self):
        weaponDamage = self.player[self.find_stat(self.player, 'Weapon')][3]
        standardDamage = self.player[self.find_stat(self.player, 'Strength')][1]
        averageDamage = weaponDamage + standardDamage
        randomDamage = int(averageDamage * 0.75) + random.randint(0, int(averageDamage/2))
        return randomDamage

    def find_stat(self, character, stat):                                                                        # returns the location of a stat or item in a player or monster
        for statIndex in range(0, len(character)):
            if character[statIndex][0] == stat:
                return statIndex
        return 'Stat not found'

    # used to call in game player stats to print
    def get_player_stats(self):
        title = 'Player:'
        player = self.player
        for stat in range(0, len(player)):
            if player[stat][0] != 'Weapon':
                title = title + '\n\n' + str(player[stat][0]) + ' = ' + str(player[stat][1])
            else:
                title = title + '\n\n' + str(player[stat][0]) + ' = ' + str(player[stat][1]) \
                        + ' ' + str(player[stat][2]) + ' ' + str(player[stat][3])
        return title

    # used to call in game monster stats to print
    def get_monster_stats(self):
        title = 'Monster: '
        monster = self.monster
        for stat in range(0, len(monster)):
            title = title + '\n\n' + str(monster[stat][0]) + ' = ' + str(monster[stat][1])
        return title

    def generate_player(self):
        self.player = self.random_stats()
        self.player.append(('Potions', random.randint(0, 5)))
        self.player.append(self.random_weapon())
        return self.player

    def generate_monster(self):
        self.monster = self.random_stats()
        return self.monster

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
        character.append(['Hit Points', hp])
        character.append(('Strength', strength))
        character.append(('Dexterity', dexterity))
        character.append(('Will', will))
        character.append(('Toughness', damageResistance))
        return character

    def random_weapon(self):
        weaponType = [('Rod', 1), ('Spear', 2), ('Axe', 3), ('Sword', 4)]
        weaponMaterial = [('Wood', 0), ('Copper', 1), ('Iron', 2), ('Adamantine', 3)]
        type = weaponType[random.randint(0, len(weaponType) - 1)]
        material = weaponMaterial[random.randint(0, len(weaponMaterial) - 1)]
        weapon = ['Weapon', material[0], type[0], type[1] + material[1]]
        return weapon

# loading files into memory

    # This function loads screens from the kv file
    def load_screens(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(BattleScreen(name='battle'))
        sm.add_widget(LogInScreen(name='login'))
        return sm

    def load_sounds(self):
        self.sounds = {}
        fileName = 'sound3.wav'
        self.sounds[0] = SoundLoader.load(fileName)

    def play_sound1(self):
        sound = self.sounds.get(0)
        if sound is not None:
            sound.volume = 0.5
            sound.play()

if __name__ == '__main__':
    MainApp().run()

