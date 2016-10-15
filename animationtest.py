from kivy.app import App
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class RootWidget(FloatLayout):
    """docstring for RootWidget"""

    def __init__(self):
        super(RootWidget, self).__init__()
        self.labelToAnimate = Label(text="Animate me")
        self.add_widget(self.labelToAnimate)
        self.labelToAnimate.pos_hint = {'x': .5, 'y': .5}
        self.animation = Animation(pos_hint={'x': 1.2, 'y': 1.2}, t="in_quad")
        self.animation.on_complete = self.anim_completed
        #self.animation.start(self.labelToAnimate)

    def anim_completed(self, animatedObj):
        print 'Completed. Restarting animation...'
        animatedObj.pos_hint = {'x': .5, 'y': .5}
        self.animation = Animation(pos_hint={'x': 1.2, 'y': 1.2}, t="in_quad")
        self.animation.on_complete = self.anim_completed
        self.animation.start(animatedObj)


class AnimTestApp(App):
    """docstring for AnimTestApp"""

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    AnimTestApp().run()
