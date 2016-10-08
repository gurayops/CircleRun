from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size


class Background(Sprite):
    """docstring for Background"""

    def update(self):
        self.x -= 2


class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.background = Background(source='images/background.png')
        # Widget boyutuna ayar verdik
        # Oyunun etrafina bir pencere, oyunun boyutunu belirliyor:
        self.size = self.background.size
        self.add_widget(self.background)
        self.add_widget(Sprite(source='images/bird.png'))
        Clock.schedule_interval(self.update, 1.0/60)

    def update(self, dt):
    	self.background.update()


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
Scroll sahnenin bir kisminin ayni anda gorulmesi icin var.
Arkaplan kayinca bosluk veya siyah kalmasin diye bir onlem almak lazim.
Disari cikanlar lazim degil.

Tek yone kaydirmak icin:
	Background'un 2 kopyasini olusturuyoruz. ikisi de bitince en basa aliyoruz.
	Bu sekilde arada GAP kalmiyor.


"""
