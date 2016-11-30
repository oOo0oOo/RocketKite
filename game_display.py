import math
import random

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import ListProperty

from game_objects import *
from utils import random_sequential
from popups import IntroPopup, PausePopup


class GameDisplay(Widget):
    color_bg = ListProperty([0.5,0.5,0.5])
    def __init__(self, **kwargs):
        super(GameDisplay, self).__init__(**kwargs)
        self.paused = True
        self.current_highscore = [-1,-1]
        self.color_theme = False
        # self.load_level()


    def return_to_main(self, next_level = False):
        self.parent.return_to_main(tuple(self.current_highscore), next_level = next_level)


    def load_level(self, params, current_highscore = (-1,-1)):
        self.current_highscore = list(current_highscore)
        self.initial_highscore = current_highscore

        self.clear_widgets()
        self.pause_game_clock()

        self.params = params
        self.sim_speedup = params['sim_speedup']


        self.setup_coord_system(params['simulation_box'])

        # Create Planets
        self.planets = []
        self.planet_screen_pos = []
        self.planet_data = zip(self.params['planet_pos'],self.params['planet_radius'],self.params['planet_mass'])

        for i, pos in enumerate(params['planet_pos']):
            pos = self.real_to_screen(pos)
            self.planet_screen_pos.append(pos)

            rad = self.real_to_screen_scalar(params['planet_radius'][i])
            img = params['planet_img'][i]
            self.planets.append(Planet(radius = rad, pos = pos, img = img, on_touch_down = self.on_planet_touch))
            self.add_widget(self.planets[-1])

            # Calculate the canon pos
            if i == params['canon_planet']:
                angle = params['canon_planet_angle']
                rad_angle = math.radians(angle)
                x = pos[0] + math.sin(rad_angle) * rad
                y = pos[1] + math.cos(rad_angle) * rad
                self.canon_pos = (x, y)

        self.canon = Canon(pos = self.canon_pos,
            angle = angle,
            max_angle = params['canon_max_angle'],
            scale = self.scale_factor)

        self.add_widget(self.canon)

        # Setup the checkpoints
        self.checkpoints = []
        for i, planet in enumerate(params['checkpoint_planet']):

            # find the start and endpoint of the checkpoint
            angle = math.radians(params['checkpoint_angle'][i])
            vect = [math.sin(angle), math.cos(angle)]
            p_pos = self.planet_data[planet][0]

            points = []
            seg = params['checkpoint_segment'][i]

            for d in seg:
                p = [p_pos[ii] + d * vect[ii] for ii in range(2)]
                points += self.real_to_screen(p)

            cp = Checkpoint(points, scale = self.scale_factor)

            self.add_widget(cp)
            self.checkpoints.append(cp)

        # Add Buttons
        border = self.size_win[0] / 60
        btn_size = (self.size_win[1]/3.6, self.size_win[1]/7.2)
        btn_size2 = (self.size_win[0]/20, self.size_win[0]/20)

        up_pos = (self.size_win[0] - border*4 - btn_size[0], border)
        down_pos = (border*4, border)

        self.accelerate_btn = FlatButton(btn_callback = self.btn_press,
            btn_name = 'up', btn_img = 'img/buttons/up.png', size = btn_size, pos = up_pos)

        self.brake_btn = FlatButton(btn_callback = self.btn_press,
            btn_name = 'down', btn_img = 'img/buttons/down.png', size = btn_size, pos = down_pos)

        self.pause_btn = AnimFlatButton(btn_callback = self.btn_press,
            btn_name = 'pause', btn_img = 'img/buttons/pause.png', size = btn_size2,
            pos = (self.size_win[0]-btn_size2[0]-border, self.size_win[1]-btn_size2[0]-border))

        self.add_widget(self.accelerate_btn)
        self.add_widget(self.brake_btn)
        self.add_widget(self.pause_btn)

        # Reward and time display
        icon_size = self.size_win[1] / 22.5
        h1 = self.size_win[1] - icon_size
        h2 = self.size_win[1] - 2.5 * icon_size
        pos_x = self.size_win[0] / 14

        self.time_disp = Label(text = '546.3', font_size=32 * self.scale_factor,
            center = (pos_x, h1))

        self.time_img = Icon(img = 'img/icons/time.png',
            pos = (15, h1-icon_size/2), size = (icon_size,icon_size))

        self.add_widget(self.time_disp)
        self.add_widget(self.time_img)

        self.kite_icons = []
        for i in range(3):
            self.kite_icons.append(Icon(img = 'img/icons/kite.png',
            pos = (15 + (i * icon_size * 1.25), h2-icon_size/2), size = (icon_size,icon_size)))
            self.add_widget(self.kite_icons[-1])

        # Add trace
        self.trace = Trace(scale = self.scale_factor)
        self.add_widget(self.trace)

        # Make kite and hide it
        self.kite = Kite(scale = self.scale_factor, pos = (0,0), velocity=(0,0), acceleration = self.params['acc'])
        self.kite.opacity = 0.0
        self.add_widget(self.kite)

        # Random scheme
        if self.color_theme:
            theme = self.color_theme
        else:
            theme = random_sequential()
        self.set_color_theme(theme)

        # This is really needed!
        self.start_launch()

        self.update_highscore()

        # Display the Introduction popup if its the first level
        title = self.params.get('intro_title', '')
        text = self.params.get('intro_text', '')
        if title:
            data = {'title': title, 'text': text}
            self.intro_popup = IntroPopup(data = data, size_hint = (0.6,0.8),
                on_dismiss = self.popup_dismissed, scale = self.scale_factor)
            self.intro_popup.open()


    def setup_coord_system(self, size_sim):
        # The simulation box is maximized and centered on the screen
        self.size_win = tuple(Window.size)

        # Scaling factor
        scale = [float(self.size_win[i]) / size_sim[i] for i in range(2)]
        scale = round(min(scale),4)

        # Transform
        scaled_sim = [int(s*scale) for s in size_sim]
        transform = [(w-s)/2 for w,s in zip(self.size_win, scaled_sim)]

        self.transform_vect = tuple(transform)
        self.scale_factor = scale


    def popup_dismissed(self, popup):
        if type(popup) == PausePopup:
            # Popup is dismissed twice bc all touch events are caught
            if not popup.returned:
                popup.returned = True
                if popup.do_next_level:
                    self.return_to_main(next_level = True)
                elif popup.do_return:
                    self.return_to_main()
                elif popup.do_restart and not self.launching:
                    self.start_launch()
                elif self.paused and self.launching:
                    self.start_game_clock()


    def show_pause_popup(self):
        self.update_highscore()
        new_time, new_points, new_level = self.check_initial_highscore()

        self.pause_popup = PausePopup(self.current_highscore, stars = self.params['stars'],
            new_time = new_time, new_points = new_points, new_level = new_level,
            size_hint = (0.6,0.8), on_dismiss = self.popup_dismissed, scale = self.scale_factor)

        self.pause_btn.stop_animation()
        self.pause_game_clock()
        self.pause_popup.open()

        # Now we reset the initial highscore to the current high score
        # (opening popup cancels blinking and resets achievements)
        self.initial_highscore = tuple(self.current_highscore)


    def btn_press(self, *args, **kwargs):
        btn_down = args[0].state == 'down'
        btn = args[0].name # This is defined to .text is not neede anymore

        # Open the pause popup
        if btn == 'pause' and btn_down:
            self.show_pause_popup()
            return

        if self.paused and btn_down and btn != 'pause':
            self.start_game_clock()

        # Trigger launch
        if self.launching and btn_down:
            self.launch_kite()

        # Process user input
        self.kite.user_input(btn, btn_down)


    def on_planet_touch(self, planet, touch):
        if not self.launching:
            vect = [planet.x - touch.x, planet.y - touch.y]
            if math.hypot(*vect) < planet.radius:
                self.start_launch()


    def launch_kite(self):
        pos, angle = self.canon.launch()

        pos = self.screen_to_real(pos)

        # Initial velocity in scaled coordinates
        vel = self.params['canon_velocity'] #/ self.scale_factor
        r = math.radians(angle)
        vect = [vel * math.sin(r), vel * math.cos(r)]

        # Set position and velocity of kite
        p = [pos[0] + vect[0], pos[1] + vect[1]]
        self.kite.pos = self.real_to_screen((pos[0] + vect[0], pos[1] + vect[1]))
        self.kite.velocity = vect

        # End launching sequence, show trace & kite
        self.launching = False
        self.trace.opacity = 1.0
        self.kite.opacity = 1.0

        # Start planet rotation
        [p.start_rotation() for p in self.planets]


    def start_launch(self):
        '''
            Start launch sequence for new kite:
                1) Reset all episode stats
                2) Start canon aim
                3) Any button triggers launch_kite()
        '''
        # Reset episode data
        self.reward = 0
        self.episode_time = 0
        self.passed_checkpoint = [False for x in self.params['checkpoint_planet']]
        self.time_complete_checkpoints = -1
        self.last_checkpoint = -1

        # Hide trace, reset text display
        self.trace.opacity = 0.0
        self.trace.reset()
        self.time_disp.text = '0'

        # Make all checkpoints active
        for c in self.checkpoints:
            c.set_active(True)

        # Hide Kite
        self.kite.opacity = 0.0

        # Stop planet rotation
        [p.stop_rotation() for p in self.planets]

        # Set random theme
        if self.color_theme == False:
            theme = random_sequential()
            self.set_color_theme(theme)

        # We are starting the launch sequence for a new kite
        self.launching = True
        self.canon.start_launch()

        if self.paused:
            self.start_game_clock()


    def update(self,dt):

        # Update blinking animation
        self.pause_btn.update(dt)

        # Update planet rotation
        for p in self.planets:
            p.update(dt)

        # Update the canon if launching
        if self.launching:
            self.canon.update(dt)

        # Update the checkpoints
        for checkpoint in self.checkpoints:
            checkpoint.update(dt)

        # Dont do anything if paused or canon launching
        if not self.paused and not self.launching:
            # Keep track of episode time
            self.episode_time += dt

            # Show the episode time in realtime if not all checkpoints
            if self.time_complete_checkpoints == -1:
                self.time_disp.text = str(int(self.episode_time))

            # Speed up the simulation a bit
            dt *= self.sim_speedup
            remove_kite = False


            # Collision: Leave screen
            p_screen = tuple(self.kite.pos)
            p = self.screen_to_real(p_screen)

            if not 0 < p_screen[0] < self.size_win[0]:
                remove_kite = True

            elif not 0 < p_screen[1] < self.size_win[1]:
                remove_kite = True

            else:
                G = self.params['gravity_constant']

                # Collision detection: planets
                planet_vect = []
                planet_dist = []
                tot_force = [0,0]
                for p_pos, radius, mass in self.planet_data:
                    vect = [p_pos[0] - p[0], p_pos[1] - p[1]]
                    dist = math.hypot(*vect)

                    planet_vect.append(vect)
                    planet_dist.append(dist)

                    # The gravity bit
                    gravity = G * mass / (dist**2)
                    tot_force[0] += dt * vect[0] * gravity / dist
                    tot_force[1] += dt * vect[1] * gravity / dist

                    if dist < radius:
                        remove_kite = True
                        break

                if not remove_kite:
                    # Move the kite
                    # Process user inputs
                    self.kite.update(dt)

                    # Update velocity
                    k = self.kite
                    vel = (k.velocity[0] + tot_force[0], k.velocity[1] + tot_force[1])
                    k.velocity = vel

                    # Update Position
                    k.pos = self.real_to_screen((p[0] + dt * vel[0], p[1] + dt * vel[1]))

                    # Collision with checkpoint
                    # Collide widget doesnt work:(

                    abs_vel = math.hypot(*k.velocity)
                    for c, cp in enumerate(self.checkpoints):
                        # Have to take all other checkpoints before retaking this one
                        # Also prevents multiple rewards during passage of the checkpoint
                        if not self.last_checkpoint == c and not self.passed_checkpoint[c]:

                            planet_id = self.params['checkpoint_planet'][c]
                            seg = self.params['checkpoint_segment'][c]

                            if seg[0]-0.5 < planet_dist[planet_id] < seg[1]+0.5:
                                v = planet_vect[planet_id]
                                angle = math.degrees(math.atan2(v[1],v[0]))
                                ca = self.params['checkpoint_angle'][c]

                                if abs((angle+ca+90)%360) < abs_vel:

                                    # Currently on checkpoint
                                    self.last_checkpoint = c

                                    # Change active checkpoints (color)
                                    cp.set_active(False)

                                    # Log checkpoint and check if first time all checkpoints
                                    before_any = any(self.passed_checkpoint)
                                    self.passed_checkpoint[c] = True

                                    if all(self.passed_checkpoint) and before_any:
                                        # Give reward
                                        self.reward += 1
                                        self.time_complete_checkpoints = self.episode_time
                                        self.passed_checkpoint = [False for i in range(len(self.checkpoints))]

                                        # Update display
                                        self.time_disp.text = str(round(self.episode_time, 1))

                                        for c in self.checkpoints:
                                            c.set_active(True)
                                            c.start_blinking()

                                        # Update the highscore
                                        self.update_highscore()

                                    break # No need to check other checkpoints


            # Hide kite if colided
            if remove_kite:
                self.kite.opacity = 0.0
                self.update_highscore()
                self.start_launch()

            # Update Trace
            if not self.launching:
                self.trace.add_point(self.kite.pos, self.kite.get_angle_rev())



    def check_initial_highscore(self):
        '''
            Compares current against initial highscore
            initial high score is only updated when you crash
        '''
        if self.current_highscore == self.initial_highscore:
            return False, False, False

        t,p = False, False
        if 0 < self.current_highscore[0] < self.initial_highscore[0]:
            t = True
        if 0 < self.current_highscore[1] > self.initial_highscore[1]:
            p = True
        l = self.initial_highscore[0] == -1 and self.current_highscore[0] > 0
        return t,p,l


    def update_highscore(self):
        t, p, l = False, False, False
        if self.time_complete_checkpoints != -1:
            if self.current_highscore[0] == -1:
                self.current_highscore[0] = self.time_complete_checkpoints
                t, l = True, True

            elif self.time_complete_checkpoints < self.current_highscore[0]:
                self.current_highscore[0] = self.time_complete_checkpoints
                t = True

        if self.reward > 0 and self.reward > self.current_highscore[1]:
            self.current_highscore[1] = self.reward
            p = True

        # Update kite score
        for i, n in enumerate(self.params['stars']):
            if self.current_highscore[1] == -1:
                self.kite_icons[i].opacity = 0.0
            elif n <= self.current_highscore[1]:
                self.kite_icons[i].opacity = 1.0
            else:
                self.kite_icons[i].opacity = 0.0

        # Start blinking if new record
        if t or p or l:
            self.pause_btn.start_animation()

        return t, p, l

    def set_color_theme(self, theme):
        if self.kite is not None:
            self.kite.color_bg = theme['kite_bg']
            self.kite.color_hl = theme['kite_hl']
            self.kite.color_rocket = theme['kite_rocket']
            self.kite.color_thrust = theme['kite_thrust']


            # Kite tail
            self.trace.tail.color_bg = theme['kite_tail']
            c1, c2 = theme['triangle_bg'], theme['triangle_hl']
            for i, t in enumerate(self.trace.triangles):
                t.color_bg = c1
                t.color_hl = c2
                c2, c1 = c1, c2 # Swap colors


        for p in self.planets:
            p.color_bg = theme['planet_bg']
            p.color_hl = theme['planet_hl']

        for p in self.checkpoints:
            p.color_bg = theme['checkpoint_bg']
            p.color_hl = theme['checkpoint_hl']

        for btn in [self.accelerate_btn, self.brake_btn, self.pause_btn]:
            btn.color_bg = theme['btn_bg']
            btn.color_hl = theme['btn_hl']

        for k in self.kite_icons:
            k.color_bg = theme['icon_bg']

        self.time_img.color_bg = theme['icon_bg']
        self.time_disp.color = list(theme['icon_bg']) + [1]

        self.canon.color_bg = theme['canon_bg']
        self.trace.color_bg = theme['trace_bg']
        self.color_bg = theme['main_bg']


    def real_to_screen_scalar(self, s):
        return float(s) * self.scale_factor


    def screen_to_real_scalar(self, s):
        return float(s) / self.scale_factor


    def screen_to_real(self, pos):
        return ((pos[0] - self.transform_vect[0]) / self.scale_factor, (pos[1] - self.transform_vect[1]) / self.scale_factor)


    def real_to_screen(self, pos):
        return (pos[0] * self.scale_factor + self.transform_vect[0], pos[1] * self.scale_factor + self.transform_vect[1])


    def pause_game_clock(self):
        self.paused = True
        Clock.unschedule(self.update)


    def start_game_clock(self):
        if not self.paused:
            print 'Why is the game clock already running?'
            self.pause_game_clock() # For good measure?

        self.paused = False
        Clock.schedule_interval(self.update, 1./60)




if __name__ == '__main__':
    game_display = GameDisplay()