# import all these things so that the .pv file can access them

import random # import random allows for random generation of values

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest

'''
Set the location and names for each of the sounds.
'''
sfx_flap = SoundLoader.load("Resources/audio/flap.wav")
sfx_score = SoundLoader.load("Resources/audio/score.wav")
sfx_die = SoundLoader.load("Resources/audio/Owl_music.wav")

'''
Create the main menu and add the background, ground and label.
Super makes sure the widget is initialised.
'''
class Menu(Widget):

    def __init__(self):
        super(Menu, self).__init__()
        self.add_widget(Sprite(source="Resources/images/metal_background.png"))
        self.size = self.children[0].size
        self.add_widget(Ground(source="Resources/images/metal_ground.png"))
        self.add_widget(Label(center=self.center, text="METAL" + "\n" + " GEAR" + "\n" + " OWL"))
        self.add_widget(Label(pos=(self.center_x-44, self.center_y-140), text="Tap to start"))


    '''
    When the user pressed down on touch screen or mouse click remove the main menu widget and add the game widget.
    '''
    def on_touch_down(self, *ignore):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Game())

class Scores(Widget):

    def __init__(self):
        super(Scores, self).__init__()
        self.add_widget(Sprite(source="Resources/images/metal_background.png"))
        self.size = self.children[0].size
        btn = Button(pos=(self.center_x-40, self.center_y), text="Get Highscore", font_size=4)
        btn.bind(on_press=self.callback)
        self.add_widget(btn)

        self.label=Label(pos=(self.center_x, self.center_y-40), text="Doesn't work", font_size='14sp')
        self.add_widget(self.label)
        self.add_widget(Ground(source="Resources/images/metal_ground.png"))

    def got_database(self, request, results):
        self.label.text(results)

    def callback(self, event):
        request = UrlRequest('http://bsccg03.ga.fal.io/?request=top_score', self.got_database)

    #def on_touch_down(self, *ignore):
        #parent = self.parent
        #parent.remove_widget(self)
        #parent.add_widget(Menu())

'''
Set the class sprite as an image and name the size of it the size of the texture of the image.
'''
class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

'''
This widget controls both the top and the bottom spikes as one set.
The top of the image is 5.5 x the size of the player.
'''
class Pipe(Widget):
    def __init__(self, pos):
        super(Pipe, self).__init__(pos=pos)
        self.top_image = Sprite(source="Resources/images/spike_top.png")
        self.top_image.pos = (self.x, self.y + 5.5 * 24)
        self.add_widget(self.top_image)
        self.bottom_image = Sprite(source="Resources/images/spike_bottom.png")
        self.bottom_image.pos = (self.x, self.y - 340)#- self.bottom_image.height)
        self.add_widget(self.bottom_image)
        self.width = self.bottom_image.width
        #self.width = self.top_image.width
        self.scored = False
    '''
    Update the spikes and moves them 2 pixels to the left.
    Set the top spike and bottom spike as the new x position.
    If the spike x position is less than 0 remove the widget.
    '''
    def update(self):
        self.x -=  2
        self.top_image.x = self.bottom_image.x = self.x
        #self.bottom_image.x = self.x
        if self.right < 0:
            self.parent.remove_widget(self)

'''
Controls all spikes.
Add spike is set to 0 which is descreases over time.
When less than 0 set a random height and x position.
Place the new spike widget and randomise the add spike variable countdown.
'''
class Pipes(Widget):
    add_pipe = 0
    def update(self, dt):
        for child in list(self.children):
            child.update()
        self.add_pipe -= dt
        if self.add_pipe < 0:
            y = random.randint(self.y + 50, self.height - 144)
            #x=self.width
            x = random.randint(self.width, self.width + 40)
            self.add_widget(Pipe(pos=(x, y)))
            self.add_pipe = random.uniform(0.5,4.0)

'''
Set the background image as a sprite and set it's size to the size of the image.
Create a duplicate of the background image and set the x position to the width of the background.
'''
class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)

    '''
    Update the image and the duplicate by moving 2 pixels to the left.
    When the image is less or equal to 0 set the image to the 0 x position
    And the image duplicate x position to the width of the image so appears offscreen.
    '''
    def update(self):
        self.image.x -= 2
        self.image_dupe.x -= 2

        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width

'''
The bird is called as a sprite and the velocity is set to 0 which is the movement in the y axis.
The gravity is set to -0.3 as it is a suitable fall speed
'''
class Bird(Sprite):
    def __init__(self, pos):
        super(Bird, self).__init__(source="atlas://Resources/images/owl_anim/wing-up", pos=pos)
        self.velocity_y = 0
        self.gravity = -.3
        #self.grounded = False

    '''
    The velocity and gravity are added to make the combined direction of the y axis.
    The altas changes the image of the bird depending on the velocity of the bird.
    '''
    def update(self):
        self.velocity_y += self.gravity
        self.velocity_y = max(self.velocity_y, -10)
        self.y += self.velocity_y
        if self.velocity_y < -4:
            self.source = "atlas://Resources/images/owl_anim/wing-up"
        elif self.velocity_y < 0:
            self.source = "atlas://Resources/images/owl_anim/wing-mid"

    '''
    When the screen is tapped or mouse is clicked increase the upward force, change the image of the bird and make sound.
    The velocity increase is 5.5 as it is a suitable y axis movement.
    '''
    def on_touch_down(self, *ignore):
        self.velocity_y = 5.5
        self.source = "atlas://Resources/images/owl_anim/wing-down"
        sfx_flap.play()

'''
The ground is called as a sprite and updated to move 2 pixels left.
When the x position is less than -24 then set the reset the position back.
This is a number that is suitable to the length of the ground sprite.
'''
class Ground(Sprite):
    def update(self):
        self.x -= 2

        if self.x < -24:
            self.x += 24

'''
All the widgets needed for the main game are added to the game widget.
Set the clock to update.
Set the label opacity for game over to be 0.
Set the bird and spike position.
Set game over to default false and score to 0.
'''
class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.background = Background(source="Resources/images/metal_background.png")
        self.size = self.background.size
        self.add_widget(self.background)
        self.ground = Ground(source="Resources/images/metal_ground.png")
        self.pipes = Pipes(pos=(0, self.ground.height), size=self.size)
        self.add_widget(self.pipes)
        self.add_widget(self.ground)
        self.score_label = Label(center_x=self.center_x,
            top=self.top - 30, text="0")
        self.add_widget(self.score_label)
        self.over_label = Label(center=self.center, opacity=0,
            text="Game Over")
        self.add_widget(self.over_label)
        self.bird = Bird(pos=(20, 40))
        self.add_widget(self.bird)
        Clock.schedule_interval(self.update, 1.0/60.0)
        self.game_over = False
        #self.grounded = False
        self.score = 0

    '''
    Update te game and each of the widgets.
    '''
    def update(self, dt):
        if self.game_over:
            return

        #if self.grounded:
            #return

        self.background.update()
        self.bird.update()
        self.ground.update()
        self.pipes.update(dt)


        #if self.bird.collide_widget(self.ground):
            #self.bird.y = 40


        #if self.bird.collide_widget(self.ground):
            #self.game_over = True

        '''
        If the bird is less than 40 in the y axis, which is the level of the ground, then set the y to 40.
        If the bird goes above the top of the screen -40 then set the top of the player to be -44 from the top.
        This stops the player from going off the screen.
        '''
        if (self.bird.y < 40):
            self.bird.y = 40
        if (self.bird.top > self.height-40):
            self.bird.top = self.height-44

        '''
        If the player collides with the spikes then set game over to true.
        If the spikes goes past the player then set scored to true and add to score.
        '''
        for pipe in self.pipes.children:
            if pipe.top_image.collide_widget(self.bird):
                self.game_over = True
            if pipe.bottom_image.collide_widget(self.bird): #was elif
                self.game_over = True
            elif not pipe.scored and pipe.right < self.bird.x:
                pipe.scored = True
                self.score += 1
                self.score_label.text = str(self.score) + " m"
                #sfx_score.play()

        '''
        If game over is true then change opacity of game over label to 1 and play music.
        Set the next event to tap or click.
        '''
        if self.game_over:
            sfx_die.play()
            self.over_label.opacity = 1
            self.bind(on_touch_down=self._on_touch_down)

    '''
    To remove game widget and return to main menu click or tap.
    '''
    def _on_touch_down(self, *ignore):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Scores())
        #parent.add_widget(Menu())

'''
This is the game app.
Set the window size.
'''
class Metal_OwlApp(App):
    def build(self):
        top = Widget()
        top.add_widget(Menu())
        Window.size = top.children[0].size
        return top

if __name__ == "__main__":
    Metal_OwlApp().run()
