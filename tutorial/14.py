import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size


class Ground(Sprite):
    """docstring for Ground"""

    def update(self):
        self.x -= 2
        if self.x < -24:
            self.x += 24


class Pipes(Widget):
    add_pipe = 0
    """
    Pipe update sirasinda pipe'lar kendilerini ekrandan
    cikinca zaten siliyordu. Burda dt delta t yani gecen zaman.
    1.5 saniye oluncaya kadar bekliyoruz. add_pipe degiskeni bunu
    sagliyor. Rastgele pozisyonu y yonunde verip ilerliyoruz.
    """

    def update(self, dt):
        for child in list(self.children):
            child.update()
        self.add_pipe -= dt

        if self.add_pipe < 0:
            # En az 50px ve ustune rastgele gelsin.
            y = random.randint(self.y + 50, self.height - 50 - 3.5 * 24)
            self.add_widget(Pipe(pos=(self.width, y)))
            self.add_pipe = 1.5


class Pipe(Widget):
    """docstring for Pipe"""

    def __init__(self, pos):
        super(Pipe, self).__init__(pos=pos)
        self.top_image = Sprite(source="images/pipe_top.png")
        # 3.5 tane kus. Bir kus 24px yuksekliginde
        self.top_image.pos = (self.x, self.y + 3.5 * 24)
        self.add_widget(self.top_image)

        self.buttom_image = Sprite(source="images/pipe_bottom.png")
        self.buttom_image.pos = (self.x, self.y - self.buttom_image.height)
        self.add_widget(self.buttom_image)

        self.width = self.top_image.width

        self.scored = False

    def update(self):
        self.x -= 2
        self.top_image.x = self.buttom_image.x = self.x
        if self.right < 0:
            self.parent.remove_widget(self)


class Bird(Sprite):
    """docstring for Bird"""

    def __init__(self, pos):
        # source="atlas://images/bird-anim/wing-up"
        super(Bird, self).__init__(source="images/bird.png",
                                   pos=pos)
        self.velocity_y = 0
        self.gravity = -.3

    def update(self):
        self.velocity_y += self.gravity
        self.velocity_y = max(self.velocity_y, -10)
        self.y += self.velocity_y
        if self.velocity_y < -5:
            self.source = "atlas://images/bird_anim/wing-up"
        elif self.velocity_y < 0:
            self.source = "atlas://images/bird_anim/wing-mid"

    def on_touch_down(self, *ignore):
        self.velocity_y = 5.5
        self.source = "atlas://images/bird_anim/wing-down"


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

        # Ground plane
        self.ground = Ground(source="images/ground.png")
        self.add_widget(self.ground)

        # Pipes
        self.pipes = Pipes(pos=(0, self.ground.height), size=self.size)
        self.add_widget(self.pipes)

        # Score
        self.score_label = Label(center_x=self.center_x,
                                 top=self.top - 30, text="0")
        self.add_widget(self.score_label)

        # Game over label
        self.over_label = Label(center=self.center, opacity=0,
                                text="Game over")
        self.add_widget(self.over_label)

        # Eski hali bu idi:
        # self.add_widget(Sprite(source='images/bird.png'))
        # Kusu ortada 20px oteden baslat
        self.bird = Bird(pos=(20, self.height / 2))
        self.add_widget(self.bird)
        Clock.schedule_interval(self.update, 1.0 / 60)

        self.game_over = False
        self.score = 0

    def update(self, dt):
        self.background.update()

        if self.game_over:
            self.over_label.opacity = 1
            return

        # Update the bird, too
        self.bird.update()
        # Update ground
        self.ground.update()
        # Update the pipes with the help of dt to get new pipes at time
        self.pipes.update(dt)
        # Check collision in order to determine game over state
        # Check whether bird is colliding with the ground
        if self.bird.collide_widget(self.ground):
            self.game_over = True

        for pipe in self.pipes.children:
            if pipe.top_image.collide_widget(self.bird) or pipe.buttom_image.collide_widget(self.bird):
                self.game_over = True
            elif (not pipe.scored) and pipe.right < self.bird.x:
                pipe.scored = True
                self.score += 1
                self.score_label.text = str(self.score)

        if self.game_over:
            print "Game Over!"
            print "Game Over! Score:", self.score


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
Durmasi gerektiginde oyunu durdur.

"""
