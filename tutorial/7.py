from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

'''
class Background(Sprite):
    """docstring for Background"""

    def update(self):
        self.x -= 2
'''


class Background(Widget):
    """docstring for Background"""

    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        # Uygulamanin en sagina aliyor, ekran disinda kalacak.
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)

    def update(self):
        self.image.x -= 2
        self.image_dupe.x -= 2

        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width


class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.background = Background(source='images/background.png')
        # Widget boyutuna ayar verdik
        # Oyunun etrafina bir pencere, oyunun boyutunu belirliyor:
        self.size = self.background.size
        self.add_widget(self.background)
        self.add_widget(Sprite(source='images/bird.png'))
        Clock.schedule_interval(self.update, 1.0 / 60)

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
Oncekinde ekran otomatik kayiyordu ama yenisi yani devami gelmiyordu.
Simdi onu duzeltiyoruz.

"""
