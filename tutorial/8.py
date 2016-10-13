from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size


class Bird(Sprite):
    """docstring for Bird"""

    def __init__(self, pos):
        super(Bird, self).__init__(source="images/bird.png", pos=pos)
        self.velocity_y = 0
        self.gravity = -.3

    def update(self):
        self.velocity_y += self.gravity
        self.velocity_y = max(self.velocity_y, -10)
        self.y += self.velocity_y

    def on_touch_down(self, *ignore):
        self.velocity = 5.5


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
        # Eski hali bu idi:
        # self.add_widget(Sprite(source='images/bird.png'))
        # Kusu ortada 20px oteden baslat
        self.bird = Bird(pos=(20, self.height / 2))
        self.add_widget(self.bird)
        Clock.schedule_interval(self.update, 1.0 / 60)

    def update(self, dt):
        self.background.update()
        # Update the bird, too
        self.bird.update()


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
