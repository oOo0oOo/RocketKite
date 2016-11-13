# The required version of the game
__version__ = '0.1'

import kivy
kivy.require('1.7.2')

from time import sleep
from math import hypot
from random import randrange

from kivy.config import Config

# Screen resolution and
Config.set('graphics', 'orientation', 'landscape')
Config.set('graphics', 'maxfps', '30')
# Config.set('postproc', 'double_tap_time', 350)
# Config.set('postproc', 'double_tap_distance', 30)

if True:
    Config.set('graphics', 'resizable', 1)
    Config.set('graphics', 'width', '1280')
    Config.set('graphics', 'height', '720')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from game_display import GameDisplay


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = GameDisplay()
        self.add_widget(self.game)

    def update(self, dt):
        self.game.update(dt)


class GameMenu(ScreenManager):
    def __init__(self):
        super(GameMenu, self).__init__(transition = WipeTransition())

        game_scr = GameScreen(name = 'game')
        self.add_widget(game_scr)

        self.current = 'game'


class SpaceApp(App):
    def build(self):
        self.game_menu = GameMenu()

        Window.bind(on_keyboard=self.hook_keyboard)
        return self.game_menu


    # Disable kivy menu
    def open_settings(self):
        pass


    def hook_keyboard(self,window,key,*largs):
        # back button behaviour
        if key == 27:
            return False

        # menu key behaviour (nothing)
        elif key in (282, 319):
            return True

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_stop(self):
        print('Stopping App')


if __name__ == '__main__' :

    '''
    try:
        import cProfile as profile
    except:
        import profile
    import pstats
    profile.run('WhiteNoiseApp().run()', 'out.stats')
    stats = pstats.Stats('out.stats')
    stats.strip_dirs()
    stats.sort_stats('tottime')
    stats.print_stats()
    '''

    SpaceApp().run()