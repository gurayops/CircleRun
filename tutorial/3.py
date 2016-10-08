from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image


class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.add_widget(Image(source='images/background.png'))
        self.add_widget(Image(source='images/bird.png'))

class GameApp(App):
    def build(self):
        # Size yazilmazsa 100,100 olarak gececek.
        return Game()


if __name__ == "__main__":
    GameApp().run()
"""
png jpg bmp direk destekliyor. Baska formatlar PIL built ini ile sahlaniyor.

Bu kod ile bos ekranda sol altta flappy bird ve ufak bir arkaplan olacak.

Image widgeti varsayilanda kendisini orantilamiyor. 100*100 varsayilan 
boyutunda widgetler icinde oluyorlar.
"""
