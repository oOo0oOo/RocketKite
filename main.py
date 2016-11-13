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
Config.set('graphics', 'maxfps', '40')
# Config.set('postproc', 'double_tap_time', 350)
# Config.set('postproc', 'double_tap_distance', 30)

if True:
    Config.set('graphics', 'resizable', 1)
    Config.set('graphics', 'width', '1280')
    Config.set('graphics', 'height', '720')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from game_display import GameDisplay
from game_objects import FlatButton
from levels import progression_levels


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = GameDisplay()
        self.add_widget(self.game)

    def load_level(self, level):
        self.game.load_level(level)

    def update(self, dt):
        self.game.update(dt)

    def on_pre_enter(self, *args):
        self.game.start_game_clock()

    def return_to_main(self):
        self.game.pause_game_clock()
        self.parent.current = 'main'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Window.clearcolor = (0.8,0.8,0.8,1.0)
        main_l = BoxLayout(orientation = 'vertical')
        btn_l = GridLayout(cols = 5, size_hint = (1,0.7),
                row_default_height = 250, row_force_default = True,
                spacing = 20, padding = 20)

        btns = []
        for i, (name, __) in enumerate(progression_levels):
            btn_img = 'img/maps/{}.png'.format(name)

            btn = Button(on_press = self.start_level)
            btn.background_color = 0.2,0.2,0.2,1.0
            btn.background_normal = btn_img
            btn.background_down = ''
            btn.name = i
            btn_l.add_widget(btn)

        title = Label(text = 'ROCKET KITE', font_size = 75, size_hint = (1,0.3),
            color = (0.2,0.2,0.2, 1.0))
        main_l.add_widget(title)
        main_l.add_widget(btn_l)

        self.add_widget(main_l)


    def start_level(self, btn):
        par = self.parent
        screen = par.get_screen('game')
        screen.load_level(progression_levels[btn.name][1])
        par.current = 'game'


class GameMenu(ScreenManager):
    def __init__(self):
        super(GameMenu, self).__init__(transition = SlideTransition(duration = 1))

        main_scr = MainScreen(name = 'main')
        game_scr = GameScreen(name = 'game')
        self.add_widget(main_scr)
        self.add_widget(game_scr)

        self.current = 'main'


class RocketKiteApp(App):
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
    profile.run('RocketKiteApp().run()', 'out.stats')
    stats = pstats.Stats('out.stats')
    stats.strip_dirs()
    stats.sort_stats('tottime')
    stats.print_stats()
    '''

    RocketKiteApp().run()