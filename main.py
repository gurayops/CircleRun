# -*-coding:utf-8-*-
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.atlas import Atlas
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.relativelayout import RelativeLayout

from math import sin, cos, radians


from kivy.core.audio import SoundLoader
directionChangeSound = SoundLoader.load("buttonSound.wav")

# Temporary window size configuration
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')


class PlayGround(Widget):
    """docstring for PlayGround"""
    radius = NumericProperty()

    def __init__(self, **kwargs):
        super(PlayGround, self).__init__(**kwargs)
        self.created = False
        # self.start()

    def on_touch_down(self, x):
        print "Playground; Radius: %s, Size: %s, Center: %s, Pos: %s" % (self.radius, self.size, self.center, self.pos), x

    def on_pos(self, x, y):
        # print x, y
        self.start()
        # print "resize"

    def start(self):
        # print "konum, boyut", self.pos, self.size, self.size_hint
        self.coins = Coins(size=self.size, pos=self.pos)
        # print "merkezler: ", self.center, self.coins.center
        self.setCoins(40)
        self.add_widget(self.coins)

    def find_location(self, angleInDegree):
        """Find position of corresponding degree"""
        angle = radians(angleInDegree)
        # self.radius = self.height / 2
        x = int(self.radius * cos(angle)) + self.center_x
        y = int(self.radius * sin(angle)) + self.center_y + 36
        print "*****", self.x, self.y, x, y, self.center, "*****"
        return x, y

    def setCoins(self, count):
        if self.created:
            return
        self.created = True
        angleBetweenCoins = 360.0 / count

        for i in range(count):
            pos = self.find_location(i * angleBetweenCoins)
            # print pos
            if i is 0:
                print "Konum: %s, aci: %s" % (pos, i * angleBetweenCoins)
            coinToAdd = Coin(center=pos)
            # print "Added, center:", pos, "coin center:", coinToAdd.center
            self.add_widget(coinToAdd)

    def update(self):
        pass


class UserObject(Widget):
    """docstring for UserObject"""

    def __init__(self):
        super(UserObject, self).__init__()


class Coin(Image):
    """docstring for Coin"""

    def __init__(self, source="images/coinGold.png", size=0, **kwargs):
        super(Coin, self).__init__(source=source, **kwargs)
        self.source = source
        # if not size:
        #    self.size = self.texture_size


class Coins(Widget):
    """docstring for Coins"""

    def __init__(self, **kwargs):
        super(Coins, self).__init__(**kwargs)

    def update(self, dt):
        for coin in self.children:
            coin.update()


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

        self.buttonPressAnimation = self.buttonExpandAnimation\
            + self.buttonShrinkAnimation
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


if __name__ == '__main__':
    CircleRun().run()
