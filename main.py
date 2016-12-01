# The required version of the game
__version__ = '1.0'

import kivy
kivy.require('1.7.2')

from time import sleep, time
from math import hypot
from random import randrange

try:
    import cPickle as pickle
except:
    import pickle

from kivy.config import Config

# Screen resolution and
Config.set('graphics', 'orientation', 'landscape')
# Config.set('graphics', 'maxfps', '100')
# Config.set('postproc', 'double_tap_time', 350)
# Config.set('postproc', 'double_tap_distance', 30)

if __name__ == '__main__':
    Config.set('graphics', 'resizable', 1)
    Config.set('graphics', 'width', '1280') #1280x720  1920x1080
    Config.set('graphics', 'height', '720')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label

from popups import IntroPopup
from game_display import GameDisplay
from game_objects import FlatButton
from levels import progression_levels
from utils import standard_color_theme, sequential_themes, theme_names, map_colors

# Register fonts
from kivy.core.text import LabelBase
LabelBase.register(name = 'fugaz',
                fn_regular = 'fonts/FugazOne-Regular.ttf')


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = GameDisplay()
        self.add_widget(self.game)

    def load_level(self, level, current_highscore):
        self.game.load_level(level, current_highscore)

    def on_pre_enter(self, *args):
        pass

    def return_to_main(self, new_highscore, next_level = False):
        self.game.pause_game_clock()
        main_screen = self.parent.get_screen('main')
        main_screen.finished_game(new_highscore)

        # Load next level (if not last)
        if next_level:
            level = main_screen.set_next_level_from_game_screen()
            if level:
                self.load_level(progression_levels[level[0]], level[1])
                return

        # Otherwise return to main screen
        main_screen.current_game = -1
        self.parent.current = 'main'

    def set_color_theme(self, theme):
        try:
            theme_ind = theme_names.index(theme)
            colors = sequential_themes[theme_ind]
            self.game.color_theme = map_colors(colors)
        except ValueError:
            self.game.color_theme = False



class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        self.last_press = 0.0 # Used for double click detection

        size_win = Window.size
        s = float(size_win[1]) / 720
        std_h = int(size_win[1] / 20.)#int(0.075 * size_win[1])
        btn_h = int(size_win[1] / 8.)

        main_l = GridLayout(cols = 1, padding = 50, spacing = 50,
            size_hint = (None, None), size = Window.size,
            pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        #main_l.bind(minimum_height=main_l.setter('height'))

        colors = [list(c) + [1] for c in standard_color_theme()]

        # title = Label(text = 'Settings', font_size = 85 * s, size_hint_y = None,
        #     height = title_y,
        #     color = colors[8])
        # main_l.add_widget(title)

        # The color selection
        color_label = Label(text = 'COLOR THEME', font_size = 40 * s, size_hint_y = None,
            height = std_h, color = colors[8])
        main_l.add_widget(color_label)

        color_dropdown = DropDown()
        tn = ['Random'] + theme_names
        st = [[(0.8,0.8,0.8)] * 5 + [(0.1,0.1,0.1)] * 4]+ sequential_themes

        color_select_btn = Button(text = 'Random',
            size_hint_y = None,
            height = btn_h,
            font_size = 40 * s,
            color = list(st[0][7]) + [1.0])
        color_select_btn.background_color = list(st[0][4]) + [1.0]
        color_select_btn.background_normal = ''
        color_select_btn.background_down = ''

        color_select_btn.bind(on_release=color_dropdown.open)
        color_dropdown.bind(on_select=lambda instance, x: setattr(color_select_btn, 'text', x))

        for name, theme in zip(tn, st):
            theme_btn = Button(text = name,
                size_hint_y = None,
                height = btn_h,
                font_size = 40 * s,
                color = list(theme[7]) + [1.0])
            theme_btn.background_color = list(theme[4]) + [1.0]
            theme_btn.background_normal = ''
            theme_btn.background_down = ''

            theme_btn.bind(on_release=lambda btn: color_dropdown.select(btn.text))
            theme_btn.bind(on_release=lambda btn: setattr(color_select_btn, 'background_color', btn.background_color))
            theme_btn.bind(on_release=lambda btn: setattr(color_select_btn, 'color', btn.color))
            color_dropdown.add_widget(theme_btn)

        self.color_select_btn = color_select_btn
        main_l.add_widget(self.color_select_btn)


        # Reset highscore
        reset_label = Label(text = 'RESET HIGHSCORE', font_size = 40 * s, size_hint_y = None,
            height = std_h,
            color = colors[8])
        main_l.add_widget(reset_label)

        btn = Button(text = 'reset (double tap)', on_press = self.reset_highscore,
            size_hint_y = None,
            height = btn_h,
            font_size = 40 * s,
            color = colors[0])
        btn.background_color = (0.6,0.1,0.1,1.0)
        btn.background_normal = ''
        btn.background_down = ''
        main_l.add_widget(btn)


        # Credits
        credits = Label(text = 'CODE & ART: Oliver Dressler', font_size = 40 * s, size_hint_y = None,
            height = std_h,
            color = colors[8])
        main_l.add_widget(credits)


        # Return btn
        btn = Button(text = 'return', on_press = self.return_to_main,
            size_hint_y = None,
            height = btn_h,
            font_size = 40 * s,
            color = colors[0])
        btn.background_color = colors[5]
        btn.background_normal = ''
        btn.background_down = ''
        main_l.add_widget(btn)
        self.add_widget(main_l)


    def reset_highscore(self, btn):
        if time() - self.last_press < 0.5:
            self.parent.get_screen('main').reset_highscore()

            data = {'title': 'RESET HIGHSCORE', 'text': 'Here we go again...'}
            popup = IntroPopup(data = data, scale = Window.size[1] / 720., size_hint = (0.6,0.8))
            popup.open()

            self.last_press = 0.0
        else:
            self.last_press = time()


    def return_to_main(self, btn):
        # Set the new color scheme
        theme = self.color_select_btn.text
        self.parent.get_screen('game').set_color_theme(theme)

        self.parent.current = 'main'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # Some responsive maths
        size_win = Window.size
        s = float(size_win[1]) / 720
        colors = standard_color_theme()
        self.colors = [list(c) + [1] for c in colors]

        title_y = int(0.2 * size_win[1])
        btn_fold = size_win[1] - title_y

        # The button is 4:5 (1/5 for stars)
        # And the grid is 4 cols
        pad_btn = 80*s
        spacing_btn = (pad_btn,120*s)
        btn_size_x = float(size_win[0]) - (pad_btn*2) - spacing_btn[0]*(3)
        btn_size_x /= 4

        # Main boxlayout and title
        main_l = GridLayout(cols = 1, padding = 10, spacing = 0, size_hint_y = None)
        main_l.bind(minimum_height=main_l.setter('height'))

        title = Label(text = 'ROCKET KITE', font_size = 85 * s, size_hint_y = None,
            height = title_y,
            color = self.colors[8])
        main_l.add_widget(title)

        # Scroll and Grid
        scroll = ScrollView(size_hint = (None,None), size = Window.size)

        btn_l = GridLayout(cols=4, spacing=spacing_btn, padding = pad_btn, size_hint_y=None)
        btn_l.bind(minimum_height=btn_l.setter('height'))

        Window.clearcolor = self.colors[2]

        # Load highscore and check which levels are available
        self.highscore = self.load_highscore()

        # Make some btns
        self.btns = []
        t = [0,3,4]
        for i, level in enumerate(progression_levels):
            btn_img = 'img/maps/{}.png'.format(level['name'])

            btn = Button(on_press = self.btn_press,
                size_hint_y = None,
                height = btn_size_x,
                font_size = 80 * s,
                color = self.colors[8])
            btn.background_color = self.colors[7]
            btn.background_normal = btn_img
            btn.background_down = ''
            btn.name = i
            btn_l.add_widget(btn)
            self.btns.append(btn)

        btn = Button(on_press = self.on_settings,
            size_hint_y = None,
            height = btn_size_x)
        btn.background_color = self.colors[6]
        btn.background_normal = 'img/buttons/settings.png'
        btn.background_down = ''

        btn_l.add_widget(btn)

        main_l.add_widget(btn_l)

        #main_l.bind(minimum_height=main_l.setter('height'))

        scroll.add_widget(main_l)
        self.add_widget(scroll)

        self.current_game = -1

        self.update_btns()


    def get_available_maps(self):
        solved = [self.highscore[i][0] != -1 for i in range(len(progression_levels))]
        return [True] + solved[:-1] # Can play one level more


    def update_btns(self):
        for i, (a, btn) in enumerate(zip(self.get_available_maps(), self.btns)):
            if a:
                btn.opacity = 1.0# self.colors[7]
            else:
                btn.opacity = 0.3# self.colors[5]

            # Update the kites (points)
            if self.highscore:
                n_kites = self.highscore[i][1]
                if n_kites == -1:
                    n_kites = 0
                elif n_kites > 3:
                    n_kites = 3
                btn.text = '\n\n' + ' '.join(['.'] * n_kites)


    def on_settings(self, btn):
        self.parent.current = 'settings'


    def btn_press(self, btn):
        self.start_level(btn.name)


    def set_next_level_from_game_screen(self):
        n = self.current_game + 1
        if n < len(progression_levels):
            self.current_game = n
            return self.current_game, self.highscore[self.current_game]

        else:
            return False


    def start_level(self, level_ind):
        # Only if level available
        if self.get_available_maps()[level_ind]:
            self.current_game = level_ind
            par = self.parent
            screen = par.get_screen('game')
            hs = self.highscore[self.current_game]
            screen.load_level(progression_levels[level_ind], hs)
            par.current = 'game'


    def finished_game(self, new_highscore):
        if self.current_game != -1:
            if self.highscore[self.current_game] != new_highscore:
                self.highscore[self.current_game] = new_highscore
                self.save_highscore()
                self.update_btns()


    def load_highscore(self, path = 'highscore.kite'):
        try:
            hs = pickle.load(open(path, 'rb'))
            assert len(hs) == len(progression_levels)
            print 'Loaded highscores:', path
            return hs
        except:
            print 'Could not load highscores:', path
            return {i: (-1,-1) for i in range(len(progression_levels))}


    def save_highscore(self, path = 'highscore.kite'):
        try:
            pickle.dump(self.highscore, open(path, 'wb'))
            print 'Saved highscores:', path
        except:
            print 'Could not save highscores:', path


    def reset_highscore(self, save = True):
        self.highscore = {i: (-1,-1) for i in range(len(progression_levels))}
        self.save_highscore()
        self.update_btns()


class GameMenu(ScreenManager):
    def __init__(self):
        super(GameMenu, self).__init__(transition = SlideTransition(duration = 0.8))

        main_scr = MainScreen(name = 'main')
        game_scr = GameScreen(name = 'game')
        settings_scr = SettingsScreen(name = 'settings')
        self.add_widget(main_scr)
        self.add_widget(game_scr)
        self.add_widget(settings_scr)

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
            if self.game_menu.current == 'main':
                return False
            elif self.game_menu.current == 'game':
                game = self.game_menu.get_screen('game').game
                if not game.paused or game.launching:
                    game.show_pause_popup()

        # menu key behaviour (nothing)
        elif key in (282, 319):
            pass

        return True

    def on_pause(self):
        game = self.game_menu.get_screen('game').game
        game.pause_game_clock()
        return True

    def on_resume(self):
        pass

    def on_stop(self):
        game = self.game_menu.get_screen('game').game
        game.pause_game_clock()
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