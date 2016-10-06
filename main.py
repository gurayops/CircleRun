# -*-coding:utf-8-*-
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.atlas import Atlas
from kivy.clock import Clock


class CircleRun(App):
    """docstring for CircleRun"""

    def __init__(self):
        super(CircleRun, self).__init__()

    # Do not close completely when app is backgrounded
    def on_pause(self):
        return True

    def build(self):
        appWindow = GameWindow()
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

    def moveUser(self, dt):
        self.ids.gamer.startLocation = (
            self.ids.gamer.startLocation + self.diff * self.level) % 360

if __name__ == '__main__':
    CircleRun().run()
