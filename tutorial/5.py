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
        self.background = Sprite(source='images/background.png')
        # Widget boyutuna ayar verdik
        self.size = self.background.size
        self.add_widget(self.background)
        self.add_widget(Sprite(source='images/bird.png'))
        # Oyunun etrafina bir pencere, oyunun boyutunu belirliyor:


class GameApp(App):
    def build(self):
        # Size yazilmazsa 100,100 olarak gececek.
        game = Game()
        # Pencere boyutu bu widget boyutu kadar olacak.
        Window.size = game.size
        return game


if __name__ == "__main__":
    GameApp().run()
"""
Oyun programlamada vazgecilmez olan Sprite'i image yerine kullanicaz.
Sprite'in yapacagi sey resmi orantilamak. Widget boyutunu icerigin boyutuna 
esitledik. Sprite'lar ekranda gozuken resimler, pozisyon ve boyutlari da var.
Resim boyutunu ve ekrandaki yerini biliyor.

Pycharm'in kivy destegi ve inspection destegi varmis.


"""
