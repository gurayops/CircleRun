# -*-coding:utf-8-*-
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.atlas import Atlas


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


class GameWindow(RelativeLayout):
    """docstring for GameWindow"""

    def __init__(self):
        super(GameWindow, self).__init__()

    def atlasTest(self):
        atlas = Atlas('images/centerMachine.atlas')
        print atlas.textures.keys()


if __name__ == '__main__':
    CircleRun().run()
