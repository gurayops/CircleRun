from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size


class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.add_widget(Sprite(source='images/background.png'))
        self.add_widget(Sprite(source='images/bird.png'))


class GameApp(App):
    def build(self):
        # Size yazilmazsa 100,100 olarak gececek.
        return Game()


if __name__ == "__main__":
    GameApp().run()
"""
Oyun programlamada vazgecilmez olan Sprite'i image yerine kullanicaz.
Sprite'in yapacagi sey resmi orantilamak.
"""
