from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


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
    def __init__(self, **kwargs):
        super(IntroPopup, self).__init__(**kwargs)

        data = {'title': 'FLY YOUR ROCKET KITE', 'text': 'pass all [b]checkpoints[/b]\nactivate [b]next level[/b]\n\ncollect [b]points[/b]\nreceive [b]MEDALS[/b]\n'}

        main_layout = BoxLayout(orientation = 'vertical', padding = 15, spacing = 25)


        main_layout.add_widget(Label(text = data['title'], font_size = 42, color = (0.1,0.1,0.1,1.0),
            h_align = 'middle', size_hint = (0.8,0.15), pos_hint = {'center_x': 0.5}))
        main_layout.add_widget(Label(text = data['text'], markup = True, color = (0.1,0.1,0.1,1.0),
            h_align = 'middle', size_hint = (0.8,0.6), font_size = 36, pos_hint = {'center_x': 0.5}))
        # main_layout.add_widget(cancel_btn)

        self.content = main_layout


    def do_protection(self, btn):
        self.dismiss()


class PausePopup(CleanPopup):
    def __init__(self, highscore, stars = [1,2,3], new_time = False, new_points = False, new_level = False, **kwargs):
        super(PausePopup, self).__init__(**kwargs)

        if new_level:
            title = 'NEW LEVEL'
        elif new_time or new_points:
            title = 'NEW HIGHSCORE!'
        else:
            title = 'HIGHSCORE'

        # Format highscore
        highscore[0] = round(highscore[0],1)
        highscore[1] = int(highscore[1])

        hs = []
        for i in highscore:
            if i != -1:
                hs.append(i)
            else:
                hs.append('-')

        n_stars = 0
        for s in stars:
            if highscore[1] < s:
                break
            n_stars += 1

        disp_stars =  '' + '*'*n_stars

        if new_time:
            hs[0] = '[color=#ADADAD]CHECKPOINTS\n{}s[/color]'.format(hs[0])
        else:
            hs[0] = 'Checkpoints\n{}s'.format(hs[0])

        if new_points:
            hs[1] = '[color=#ADADAD]KITES\n{}   {}[/color]'.format(hs[1], disp_stars)
        else:
            hs[1] = 'Kites\n{}    {}'.format(hs[1], disp_stars)

        text = '{}\n\n{}'.format(hs[1], hs[0])

        if new_level:
            text += '\n[size=25]Check out the new level[/size]'

        data = {'title': title, 'text': text}

        main_layout = BoxLayout(orientation = 'vertical', padding = 15, spacing = 25)
        btn_layout = BoxLayout(orientation = 'horizontal', padding = 10, spacing = 20)

        menu_btn = Button(text = 'MENU', on_press = self.return_to_menu,
            size_hint = (0.6,0.6), font_size = 25)
        restart_btn = Button(text = 'RESTART', on_press = self.restart,
            size_hint = (0.6,0.6), font_size = 25)

        btn_layout.add_widget(menu_btn)
        btn_layout.add_widget(restart_btn)

        main_layout.add_widget(Label(text = data['title'], font_size = 42, color = (0.1,0.1,0.1,1.0),
            halign = 'center', valign='middle', size_hint = (0.8,0.1), pos_hint = {'center_x': 0.5}))
        main_layout.add_widget(Label(text = data['text'], markup = True, color = (0.1,0.1,0.1,1.0),
            halign = 'center', valign='middle', size_hint = (0.8,0.9), font_size = 36, pos_hint = {'center_x': 0.5}))

        main_layout.add_widget(btn_layout)
        self.content = main_layout
        self.do_return = False
        self.do_restart = False


    def restart(self, btn):
        self.do_restart = True
        self.dismiss()


    def return_to_menu(self, btn):
        self.do_return = True
        self.dismiss()