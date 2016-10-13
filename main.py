# -*-coding:utf-8-*-
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.atlas import Atlas
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from math import sin, cos, radians


from kivy.core.audio import SoundLoader
directionChangeSound = SoundLoader.load("buttonSound.wav")

# Temporary window size configuration
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')


class CircleRun(App):
    """docstring for CircleRun"""

    def __init__(self):
        super(CircleRun, self).__init__()

    # Do not close completely when app is backgrounded
    def on_pause(self):
        return True

    def build(self):
        appWindow = Game()
        return appWindow


class GameWindow(BoxLayout):
    """docstring for GameWindow"""

    def __init__(self):
        super(GameWindow, self).__init__()
        # Determine the level of the game

    def atlasTest(self):
        atlas = Atlas('images/centerMachine.atlas')
        print atlas.textures.keys()

    def startMove(self):
        print "action started."
        self.diff = -1 if self.ids.gamer.direction == 1 else 1
        self.ids.gamer.direction = self.diff
        Clock.unschedule(self.moveUser)
        Clock.schedule_interval(self.moveUser, 1.0 / 60)

    def startAnimation(self):
        print "Animation started"
        pass

    def animateX(self, instance):
        animation = Animation(pos=(0, 0), t='out_sine')
        animation += Animation(pos=(400, 400), t='out_sine')
        # animation += Animation(pos=(200, 200), t='in_circ')
        # animation &= Animation(size_hint=(.3, .3))
        # animation += Animation(size_hint=(.5, .5))
        animation.start(instance)

    def stopAnimation(self):
        print "Animation has ended"
        pass

    def moveUser(self, dt):
        self.ids.gamer.startLocation = (
            self.ids.gamer.startLocation + self.diff * self.level) % 360


class PlayGround(Widget):
    """docstring for PlayGround"""

    def find_location(self, angleInDegree):
        """Find position of corresponding degree"""
        angle = radians(angleInDegree)
        x = int(self.radius * cos(angle))
        y = int(self.radius * sin(angle))
        return x, y

    def update(self):
        pass


class UserObject(Widget):
    """docstring for UserObject"""

    def __init__(self):
        super(UserObject, self).__init__()


class Coin(Image):
    """docstring for Coin"""

    def __init__(self, source="images/coinGold.png", size=0):
        super(Coin, self).__init__(source=source)
        self.source = source
        if not size:
            self.size = self.texture_size


class Enemy(Image):
    def __init__(self, source="images/flyFly1.png", size=0):
        super(Coin, self).__init__(source=source)
        self.source = source
        if not size:
            self.size = self.texture_size


class Game(FloatLayout):
    """Main game structure"""

    def __init__(self):
        super(Game, self).__init__()
        self.buttonExpandAnimation = Animation(
            size_hint=(.35, .35), t="out_sine",
            d=.2)
        self.buttonShrinkAnimation = Animation(
            size_hint=(.3, .3), t="out_sine",
            d=.2)

        self.buttonPressAnimation = self.buttonExpandAnimation + self.buttonShrinkAnimation
        self.buttonPressAnimation.repeat = "True"

    def startTurn(self, button):
        self.buttonPressAnimation.start(button)
        directionChangeSound.play()
        print button.size, button.pos
        print self.width, self.width

    def stopTurn(self, button):
        self.score += 1
        self.buttonPressAnimation.cancel(button)
        # self.buttonShrinkAnimation.start(button)

    def update(self):
        pass


if __name__ == '__main__':
    CircleRun().run()
