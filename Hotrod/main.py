import random
import os
import sys

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_sdl2 import SoundSDL2

import direction
import level
import level_cell
import character
import user_interface

# Game to run at 60 frames per second
FPS = 60
# The relative location of the game's sound files
SOUND_DIRECTORY = "sound"

# The player always starts with 3 lives
INITIAL_LIVES = 3
# The player's score always starts at 0
INITIAL_SCORE = 0

# This is a separate widget because I intend to make HotrodGame into a layout
class PlayArea(Widget):
    """Widget for the gameplay area. Gameplay objects are children of this widget."""

    def start_game(self):
        """Start the game.

        This method begins the game.
        This method should be called when a game starts.
        That is, on first start, after a game over, or on
        a new level.
        """

        self.set_up_level()
        jingle = self.game.sounds['jingle']
        jingle.play()
        # Gameplay doesn't proceed until the jingle has finished
        jingle.bind(on_stop=self.start_updates)

    def set_up_level(self):
        """Set up the level and characters.

        This method initialises the generates the level and
        initialises the characters. It should be called when
        a new game or level starts.
        """

        self.generate_level()
        self.initialise_characters()

    def generate_level(self):
        """Generate the level.

        This method procedurally generates the maze to be
        used for the level. It should be called when a new
        game or level starts.
        """

        seed = random.randint(0, sys.maxint)
        print seed
        random.seed(seed)
        self.game.level.generate_level()

    def initialise_characters(self):
        """Initialise the characters' size and positions.

        This method ensures the enemies and player's size is correct,
        as well as setting them to their starting positions. It should be
        called when a new game or level is started, as well as
        when the player dies.
        """

        self.game.player.initialise(self.game.player.start_position)
        for enemy in self.game.enemies:
            starting_cell = random.choice(self.game.level.beetle_house.values())
            enemy.initialise(starting_cell.coordinates)

    def start_updates(self, event):
        """Start the game updating.

        This method begins the actual gameplay. It schedules
        the updates and begins the enemy's mode timers. It should
        be called when a new game or level starts.
        """

        self.start_enemy_timers()
        self.game.game_active = True

    def update(self, dt):
        """Update the game state.

        This method should be called once every frame. It updates the
        state of the game, in this case, the characters' positions.
        """

        self.game.player.move()
        for enemy in self.game.enemies:
            if enemy.dead:
                enemy.retreat()
            else:
                enemy.move()

    def update_play_area(self, instance, value):
        """Ensure that game element sizes are correct.

        This Kivy event is triggered when level size changes to ensure
        that all elements of the play area are positioned and sized correctly
        """

        for column in self.game.level.cells:
            for cell in column:
                cell.update_cell()

        for enemy in self.game.enemies:
            enemy.update_character()
        self.game.player.update_character()

    def start_enemy_timers(self):
        """Start the timers for the enemies' mode changes.

        This method initialises the timers that count down
        to the enemies mode changes. This includes the timer
        between scatter/chase mode change, and the timer that
        determines when they are released. It should be called
        when a new game or level is started.
        """

        for enemy in self.game.enemies:
            enemy.reset_scatter_timers()
            enemy.reset_release_timers()

    def reset_after_death(self, event):
        """Reset the characters' positions and reset the scatter timer.

        This method both resets the characters' positions as well
        as resetting the enemies' scatter mode change timers.
        It should only be called when the player has lost a life
        without it resulting in a game over."""

        self.initialise_characters()
        for enemy in self.game.enemies:
            enemy.reset_scatter_timers()

        self.game.game_active = True


class HotrodGame(Widget):
    """Manage the game and application.

    This widget manages and controls the application.
    This widget has access to all major gameplay widgets, in addition
    to general game properties such as score and lives.
    Gameplay widgets access each other through this widget.
    """

    # Reference to the play area
    play_area = ObjectProperty(None)
    # Reference to the level
    level = ObjectProperty(None)
    # Reference to the player
    player = ObjectProperty(None)
    # List containing references to the enemies
    enemies = ListProperty()

    score = NumericProperty(INITIAL_SCORE)
    lives = NumericProperty(INITIAL_LIVES)

    pellet_value = NumericProperty(10)
    powerup_length = NumericProperty(10)

    # GUI elements so that they can be referred to in
    # multiple methods
    game_over_screen = ObjectProperty(None)
    heads_up_display = ObjectProperty(None)

    # Dictionary containing all sounds used in the game
    sounds = ObjectProperty()

    game_active = BooleanProperty(False)

    def start(self):
        """Start the game.

        This method begins game progression."""

        self.play_area.start_game()

    def load_sounds(self):
        """Load the sounds used in the game.

        This method loads the sounds for use in the game and
        stores them in a dictionary for easy access.
        """

        self.sounds = {}
        # Dictionary keys correspond to filenames
        for file in os.listdir(SOUND_DIRECTORY):
            filename, extension = os.path.splitext(file)
            key = filename
            self.sounds[key] = SoundSDL2(source=(os.path.join(SOUND_DIRECTORY, file)))

    def on_touch_up(self, touch):
        """Detect player swipes and change character's next direction accordingly

        This method detects swipes from the player and sets the player character's
        next direction to be the direction of the swipe.
        """

        # Dividing by 10 means the swipe needs to be at least a 10th of the window
        # Move right if player swipes right
        if touch.pos[0] > touch.opos[0] + self.width/10:
            self.player.next_direction = direction.Direction.right
        # Move left if player swipes left
        if touch.pos[0] < touch.opos[0] - self.width/10:
            self.player.next_direction = direction.Direction.left
        # Move up is player swipes up
        if touch.pos[1] > touch.opos[1] + self.height/10:
            self.player.next_direction = direction.Direction.up
        # Move down if player swipes down
        if touch.pos[1] < touch.opos[1] - self.height/10:
            self.player.next_direction = direction.Direction.down

    def on_lives(self, instance, value):
        """Reset the play area if a life is lost or show game over screen if all are lost.

        Kivy event called when number of lives changes. The play area is reset upon
        losing a life. If all lives are lost, the game stops and the game over
        screen is displayed.
        """

        if self.game_active:
            self.game_active = False

            if self.lives <= 0:
                game_over_sound = self.sounds['game_over']
                game_over_sound.bind(on_stop = self.show_game_over_screen)
                self.sounds['game_over'].play()
            else:
                death_sound = self.sounds['death']
                death_sound.bind(on_stop = self.play_area.reset_after_death)
                self.sounds['death'].play()

    def on_game_active(self, instance, value):
        """Start and stop game updates.

        This kivy event responds to changes in the boolean that
        states whether the game is active or not. If the game becomes
        active, updates are scheduled. If the game becomes inactive,
        updates are unscheduled."""
        if self.game_active:
            Clock.schedule_interval(self.play_area.update, 1/FPS)
        else:
            Clock.unschedule(self.play_area.update)

    def show_game_over_screen(self, event):
        """Show the game over screen.

        This method shows the game over screen. The game over screen
        is displayed until the reset button is pressed.
        """

        self.game_over_screen = user_interface.GameOverScreen()
        self.game_over_screen.size = self.size
        self.game_over_screen.center = self.center
        self.add_widget(self.game_over_screen)
        self.game_over_screen.reset_button.bind(on_press=self.reset)
        # Make sure size and position of game over screen match any window changes
        self.bind(size=self.game_over_screen.set_size)

    def reset(self, event):
        """Reset the game after a game over.

        This method removes the game over widget and resets
        the score and lives count before restarting the game.
        """

        self.remove_widget(self.game_over_screen)
        self.unbind(size=self.game_over_screen.set_size)
        self.score = INITIAL_SCORE
        self.lives = INITIAL_LIVES
        self.start()


class HotrodApp(App):
    # game is property so that it can be referred to
    # outside of build()
    game = ObjectProperty(None)

    def build(self):
     #   Config.set('graphics', 'fullscreen', 'auto')
        self.game = HotrodGame()
        return self.game

    def on_start(self):
        # Called here rather than in build() so that size is correct
        self.game.load_sounds()
        self.game.start()


if __name__ == '__main__':
    HotrodApp().run()