# -*-coding:utf-8-*-
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader as SingleSoundLoader
from kivy.properties import NumericProperty

from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.utils import platform

from math import sin, cos, radians
from random import uniform, choice


class SoundLoader(object):
    """docstring for MultiSound"""

    def __init__(self, file, num):
        self.sounds = [SingleSoundLoader.load(file) for i in range(num)]
        self.num = num
        self.index = 0

    def play(self):
        self.sounds[self.index].play()
        self.index += 1
        if self.index == self.num:
            self.index = 0


directionChangeSound = SoundLoader("audio/buttonClickSound.wav", 10)
coinSound = SoundLoader("audio/coinSound.wav", 10)

if platform in ['win', 'linux', 'macosx']:
    # Default window size configuration
    from kivy.config import Config
    Config.set('graphics', 'width', '1280')
    Config.set('graphics', 'height', '720')


class PlayGround(FloatLayout):
    """docstring for PlayGround"""
    # Radius of main circle
    radius = NumericProperty()

    def __init__(self, **kwargs):
        super(PlayGround, self).__init__(**kwargs)

        # Container for all the objects
        self.circle = CircleObjects(size_hint_y=1, size_hint_x=None, pos_hint={
            'center_x': 0.5, 'center_y': 0.5})
        self.count = 40
        self.setCoins(self.count)
        self.add_widget(self.circle)

        pos_hint = self.find_ratio(90)
        self.user = UserObject(angle=90, pos_hint={'center_x': pos_hint[
            0], 'center_y': pos_hint[1]}, size_hint=(.1, .1))
        self.circle.add_widget(self.user)

        self.enemies = Enemies(size_hint_y=1, size_hint_x=1, pos_hint={
            'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.enemies)

    def find_ratio(self, angleInDegree):
        """Find position of corresponding degree"""
        angle = radians(angleInDegree)
        # Using +1 offset in order to put the result in the range of 0 and 1
        x = (cos(angle) + 1) / 2
        y = (sin(angle) + 1) / 2
        return x, y

    def setCoins(self, count):
        """
        Add objects around the circle with equal space.
        """
        count += 1
        angleBetweenCoins = 360.0 / count

        for i in range(count):
            # Calculate the relative position
            pos_hint = self.find_ratio(i * angleBetweenCoins)

            # This is start location of user
            if i == count / 4:
                continue

            # Create coin widget with .1 size ratio
            coinToAdd = Coin(pos_hint={'center_x': pos_hint[
                             0], 'center_y': pos_hint[1]}, size_hint=(.1, .1))
            # Add current coin to the circle
            self.circle.add_widget(coinToAdd)

    def update(self):
        self.circle.update(self.user)

        # If gameover happens, stop the game
        if self.enemies.update(self.user) == -1:
            return -1

        # The last will be user, so the level ends here.
        if len(self.circle.children) == 1:
            return 1


class UserObject(Image):
    """docstring for UserObject"""
    # Direction of user object
    direction = NumericProperty(0)
    angle = NumericProperty(90)

    def __init__(self, angle, source="images/user.zip", anim_delay=.1,
                 **kwargs):
        super(UserObject, self).__init__(**kwargs)
        self.source = source
        self.anim_delay = anim_delay
        self.angle = angle
        self.difference = 1

    def changeDirection(self):
        self.direction = 0 if self.direction == 1 else 1

    def on_angle(self, *ignore):
        pos_hint = self.parent.parent.find_ratio(self.angle)
        self.pos_hint = {'center_x': pos_hint[0], 'center_y': pos_hint[1]}

    def update(self):
        # Go to new position by saying angle.
        # Consider looking on_angle for details
        if self.direction == 0:
            self.angle -= self.difference
        elif self.direction == 1:
            self.angle += self.difference
        self.size = self.texture_size


class CircleObjects(FloatLayout):
    """docstring for Coins"""

    def __init__(self, **kwargs):
        super(CircleObjects, self).__init__(**kwargs)

    def update(self, user):
        for child in self.children:
            if type(child) == Coin:
                child.update()
                if user.collide_widget(child):
                    self.remove_widget(child)
                    self.parent.parent.score += 1
                    coinSound.play()

            elif type(child) == UserObject:
                # here is user object
                child.update()


class Coin(Image):
    """docstring for Coin"""

    def __init__(self, source="images/coinGold.png", size=0, **kwargs):
        super(Coin, self).__init__(source=source, **kwargs)
        self.source = source

    def update(self):
        pass


class Enemies(FloatLayout):
    """docstring for Enemies"""

    def __init__(self, **kwargs):
        super(Enemies, self).__init__(**kwargs)
        self.allEnemies = self.set_enemies()
        self.set_positions(self.allEnemies)

        for enemy in self.allEnemies:
            self.add_widget(enemy)

        self.userAngle = 90
        self.userAngleDiff = 1
        # Duration of animation
        self.duration = 1

        # self.anim_ts = ('in_elastic', 'in_out_bounce',
        #                'out_back', 'out_bounce')
        self.anim_ts = ['in_quad']

    def set_enemies(self):
        # Todo: Make enemy count a parameter.
        self.enemy_1 = Enemy(size_hint_y=.05, size_hint_x=None,
                             pos_hint={'x': .5, 'y': .5})
        self.enemy_2 = Enemy(size_hint_y=.05, size_hint_x=None,
                             pos_hint={'x': .5, 'y': .5})
        self.enemy_3 = Enemy(size_hint_y=.05, size_hint_x=None,
                             pos_hint={'x': .5, 'y': .5})
        return [self.enemy_1, self.enemy_2, self.enemy_3]

    def set_positions(self, enemies):
        for enemy in enemies:
            enemy.pos_hint = {'center_x': .5, 'center_y': .5}

    def get_remaining_count(self):
        '''
        Gets number of enemy elements that are available.

        Useful for finding whether the current level is completed.
        '''
        return len(self.allEnemies)

    def update(self, user):
        self.userAngle = user.angle
        self.userAngleDiff = user.difference
        for child in self.allEnemies:
            child.update()
            # Game Over is Determined Here
            if child.collide_widget(user):
                self.anim1.cancel(self.enemy_1)
                self.anim2.cancel(self.enemy_2)
                self.anim3.cancel(self.enemy_3)
                return -1

    def find_ratio(self, angleInDegree):
        """Find position of corresponding degree"""
        angle = radians(angleInDegree)
        # Using +1 offset in order to put the result in the range of 0 and 1
        # rand lines adds some randomness
        x = (cos(angle) + 1) / 2
        rand_x = uniform(x / -20, x / 20) + x
        y = (sin(angle) + 1) / 2
        rand_y = uniform(y / -20, y / 20) + y
        return rand_x, rand_y

    def anim_completed(self, enemy):
        self.set_positions([enemy])

        # Target angle 1
        t1 = self.find_ratio(
            self.userAngle + self.userAngleDiff * 60 * self.duration)
        t2 = self.find_ratio(
            self.userAngle - self.userAngleDiff * 60 * self.duration)
        t3 = self.find_ratio(self.userAngle)

        # Restart the animations
        if enemy == self.enemy_1:
            self.anim1 = Animation(pos_hint={'center_x': t1[0],
                                             'center_y': t1[1]},
                                   t=choice(self.anim_ts), d=self.duration)
            self.anim1.on_complete = self.anim_completed
            self.anim1.start(self.enemy_1)
        elif enemy == self.enemy_2:
            self.anim2 = Animation(pos_hint={'center_x': t2[0],
                                             'center_y': t2[1]},
                                   t=choice(self.anim_ts), d=self.duration)
            self.anim2.on_complete = self.anim_completed
            self.anim2.start(enemy)
        elif enemy == self.enemy_3:
            print "Anim 3 completed, restarting..."
            self.anim3 = Animation(pos_hint={'center_x': t3[0],
                                             'center_y': t3[1]},
                                   t=choice(self.anim_ts), d=self.duration)
            self.anim3.on_complete = self.anim_completed
            self.anim3.start(enemy)

    def fire(self):
        """Fires 3 enemies"""
        print "Anim fired..."
        # self.anim1 = Animation(pos_hint=(.8, .8), t="in_quad")
        self.anim1 = Animation(
            pos_hint={'center_x': 1.2, 'center_y': 1.2}, t="in_quad")
        self.anim2 = Animation(
            pos_hint={'center_x': 1.2, 'center_y': 1.2}, t="in_quad")
        self.anim3 = Animation(
            pos_hint={'center_x': 1.2, 'center_y': 1.2}, t="in_quad")
        self.anim1.on_complete = self.anim_completed
        self.anim2.on_complete = self.anim_completed
        self.anim3.on_complete = self.anim_completed
        self.anim1.start(self.enemy_1)
        self.anim2.start(self.enemy_2)
        self.anim3.start(self.enemy_3)


class Enemy(Image):
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(allow_stretch=True,
                                    source="atlas://images/bird_anim/wing-up",
                                    **kwargs)
        size = self.texture_size
        if not size:
            self.size = self.texture_size
        self.state = 1

    def update(self):
        """
        Enemy effects related to bird_anim atlas.
        Consists of 3 images.
        """
        if self.state is 1:
            self.source = "atlas://images/bird_anim/wing-up"
        elif self.state is 2:
            self.source = "atlas://images/bird_anim/wing-mid"
        elif self.state is 3:
            self.source = "atlas://images/bird_anim/wing-down"
        self.state += 1
        if self.state == 4:
            self.state = 1

    def on_texture_size(self, x, y):
        """
        Arranges the image size according to source image
        """
        self.size = self.texture_size


class Game(FloatLayout):
    """Main game structure"""
    score = NumericProperty(0)

    def __init__(self, level):
        super(Game, self).__init__()
        self.buttonExpandAnimation = Animation(
            size_hint=(.35, .35), t="out_sine",
            d=.1)
        self.buttonShrinkAnimation = Animation(
            size_hint=(.3, .3), t="in_sine",
            d=.1)

        # Determine the game is started or not when the widget is created
        self.playing = False

        # Determine if the game is ended
        self.gameOver = False

        # Level and level-dependent calculations
        self.level = level
        # Calculate score at beginning
        self.score = self.level * 40
        self.updateSpeed = self.level * 5 + 60

        # Update method
        self.timer = Clock.schedule_interval(
            self.update, 1.0 / self.updateSpeed)

        # Was used for continuous animation. No need anymore and
        # not working well
        # self.buttonPressAnimation = self.buttonExpandAnimation\
        #    + self.buttonShrinkAnimation
        # self.buttonPressAnimation.repeat = "True"

    def startTurn(self, button):
        self.buttonShrinkAnimation.cancel_all(button)
        self.buttonExpandAnimation.start(button)
        directionChangeSound.play()

        self.ids.pg.user.changeDirection()

        if not self.playing:
            self.playing = True
            self.ids.pg.enemies.fire()

    def stopTurn(self, button):
        self.buttonExpandAnimation.cancel_all(button)
        self.buttonShrinkAnimation.start(button)

    def update(self, *ignore):
        # If gameover happened, stop timers and add main window
        # as our new root widget.
        if self.gameOver:
            self.timer.cancel()
            parent = self.parent
            # Make ResultScreen class the root
            parent.remove_widget(self)
            parent.add_widget(ResultScreen(self.score))

        # Return if the game is not continuing or has not started
        if self.playing == 0:
            return

        # Update the playground
        # 1 => Level completed, -1 => Game over.
        updateResult = self.ids.pg.update()

        if updateResult == -1:
            self.gameOver = 1
        elif updateResult == 1:
            self.playing = 0
            self.timer.cancel()
            parent = self.parent
            # Make ResultScreen class the root
            parent.remove_widget(self)
            parent.add_widget(Game(self.level + 1))


class ResultScreen(BoxLayout):
    def __init__(self, lastScore, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.lastScore = lastScore

    def changeMainWidget(self, newObj):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(newObj)

    def goMainMenu(self):
        self.changeMainWidget(Menu())

    def newGame(self):
        self.changeMainWidget(Game(0))


class Menu(FloatLayout):
    """TODO: Make this a widget and add some graphics"""

    def __init__(self):
        super(Menu, self).__init__()
        self.menuAnim = Animation(size_hint_y=.7, t='out_quint',
                                  duration=.5) + \
            Animation(size_hint_y=.6, t='in_quart', duration=.5)
        self.menuAnim.repeat = True
        self.menuAnim.start(self.ids.playButton)

    def on_start(self):
        '''
        Starts a new game.
        '''
        root = self.parent
        root.remove_widget(self)
        root.add_widget(Game(0))

    def high_scores(self):
        self.changeMainWidget(HighScores())

    def changeMainWidget(self, newObj):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(newObj)


class HighScores(BoxLayout):
    def __init__(self):
        super(HighScores, self).__init__()

    def changeMainWidget(self, newObj):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(newObj)

    def main_menu(self):
        self.changeMainWidget(Menu())


class CircleRun(App):
    """docstring for CircleRun"""

    def __init__(self):
        super(CircleRun, self).__init__()

    # Do not close completely when app is backgrounded
    def on_pause(self):
        return True

    def build(self):

        appWindow = FloatLayout()
        # Start directly into a new game
        # appWindow.add_widget(Game())
        appWindow.add_widget(Menu())
        return appWindow


if __name__ == '__main__':
    CircleRun().run()
