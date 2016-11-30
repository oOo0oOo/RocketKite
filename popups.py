from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from levels import n_levels


class CleanPopup(Popup):
    def __init__(self, **kwargs):
        default_params = {
            'title': '',
            'separator_height': 0,
            'title_size': 0,
            'auto_dismiss': True,
            # 'background_color': (0,0,0,0.3)
            }
        kwargs.update(default_params)
        super(CleanPopup, self).__init__(**kwargs)

        # Replace the original Popup
        self.border = (0,0,0,0)
        self.background = 'img/unicolor.png'
        self.background_color = (0.3,0.3,0.3,0.3)


class IntroPopup(CleanPopup):
    def __init__(self, data = {}, scale = 1.0, **kwargs):
        super(IntroPopup, self).__init__(**kwargs)

        # data = {'title': 'ROCKET KITE', 'text': 'To activate [b]next level[/b]\npass all [b]checkpoints[/b]\n\n\nCollect [b]kites[/b]\nget [b]STARS[/b]\n'}
        if not data:
            data = {'title': '', 'text': ''}

        main_layout = BoxLayout(orientation = 'vertical', padding = 15 * scale, spacing = 25 * scale)

        main_layout.add_widget(Label(text = data['title'], font_size = 42 * scale, color = (0.1,0.1,0.1,1.0),
            h_align = 'middle', size_hint = (0.8,0.15), pos_hint = {'center_x': 0.5}))
        main_layout.add_widget(Label(text = data['text'], markup = True, color = (0.1,0.1,0.1,1.0),
            h_align = 'middle', size_hint = (0.8,0.6), font_size = 36 * scale, pos_hint = {'center_x': 0.5}))
        self.content = main_layout


    def on_touch_down(self, *args):
        self.dismiss()


class PausePopup(CleanPopup):
    def __init__(self, highscore, new_time = False, new_points = False, new_level = False, scale = 1.0, **kwargs):
        super(PausePopup, self).__init__(**kwargs)

        self.returned = False

        if new_level:
            title = 'NEW LEVEL!'
        elif new_time or new_points:
            title = 'NEW HIGHSCORE!'
        else:
            title = 'HIGHSCORE'

        # Format highscore
        highscore[0] = round(highscore[0],1)
        highscore[1] = int(highscore[1])

        if highscore[1] == -1:
            n_kites = 0
        else:
            n_kites = highscore[1]

        if highscore[0] == -1:
            n_sec = '-'
        else:
            n_sec = str(highscore[0])

        hs = ['','']

        if new_time:
            hs[0] = '[color=#ADADAD]CHECKPOINTS\n{}s[/color]'.format(n_sec)
        else:
            hs[0] = 'CHECKPOINTS\n{}s'.format(n_sec)

        if new_points:
            hs[1] = '[color=#ADADAD]KITES\n{}[/color]'.format(n_kites)
        else:
            hs[1] = 'KITES\n{}'.format(n_kites)

        text = '{}\n{}'.format(hs[1], hs[0])

        # if new_level:
        #     text += '\n[size=12]Check out the new level[/size]'

        data = {'title': title, 'text': text}

        main_layout = BoxLayout(orientation = 'vertical', padding = 5 * scale, spacing = 75 * scale)
        btn_layout = BoxLayout(orientation = 'horizontal', padding = 10 * scale, spacing = 20* scale)

        menu_btn = Button(text = 'MENU', on_press = self.return_to_menu,
            size_hint = (0.6,0.6), font_size = 25* scale)
        restart_btn = Button(text = 'RESTART', on_press = self.restart,
            size_hint = (0.6,0.6), font_size = 25* scale)

        btn_layout.add_widget(menu_btn)
        btn_layout.add_widget(restart_btn)

        if highscore[0] != -1:
            level_btn = Button(text = 'NEXT LEVEL', on_press = self.new_level,
                size_hint = (0.6,0.6), font_size = 25* scale)
            btn_layout.add_widget(level_btn)

        main_layout.add_widget(Label(text = data['title'], font_size = 42* scale, color = (0.1,0.1,0.1,1.0),
            halign = 'center', size_hint = (0.8,0.3), pos_hint = {'center_x': 0.5}))
        main_layout.add_widget(Label(text = data['text'], markup = True, color = (0.1,0.1,0.1,1.0),
            halign = 'center', size_hint = (0.8,0.3), font_size = 36* scale, pos_hint = {'center_x': 0.5, 'center_y': 0.5}))

        main_layout.add_widget(btn_layout)
        self.content = main_layout
        self.do_return = False
        self.do_restart = False
        self.do_next_level = False


    def on_touch_down(self, *args):
        super(PausePopup, self).on_touch_down(*args)
        self.dismiss()


    def restart(self, btn):
        self.do_restart = True
        self.dismiss()


    def new_level(self, btn):
        self.do_next_level = True
        self.dismiss()


    def return_to_menu(self, btn):
        self.do_return = True
        self.dismiss()