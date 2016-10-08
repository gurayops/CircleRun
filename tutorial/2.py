from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window


class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        with self.canvas:
            Color(.5, .5, 1.0)
            Rectangle(pos=(0, 0), size=self.size)


class GameApp(App):
    def build(self):
    	# Size yazilmazsa 100,100 olarak gececek.
        return Game(size=Window.size)


if __name__ == "__main__":
    GameApp().run()
"""
Ilk kod bos oyun ekrani olusturmustu. Bu kod biraz grafik ekleyecek.

Ilk olarak init fonksiyonunun uzerine yazildi. super fonksiyonunu unutursak 
duzgun baslatilma islemi yapilamaz.

Sonra canvas islemleri yapiliyor. Once renk rectik sonra bu renkle dikdortgen cizdik.
Canvas'ta bir degisiklik yapmak cok sey degistirebiliyor.

Basit bir mavi kod karsilayacak. Sol alt kisim 0,0 noktasi kabul ediliyor.    

Color icin alternatif:
from kivy.utils import get_color_from_hex
green = get_color_from_hex('#00ff00')
Color(*green)

Grafik icin Color ve Rectangle eklendi.

"""
