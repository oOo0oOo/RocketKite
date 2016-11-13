import math
import random

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import ListProperty

from game_objects import *
from levels import progression_levels
from utils import random_diverging, random_sequential


class GameDisplay(Widget):
    color_bg = ListProperty([0.5,0.5,0.5])
    def __init__(self, **kwargs):
        super(GameDisplay, self).__init__(**kwargs)
        self.load_level()


    def load_level(self, params = False):
        self.clear_widgets()
        self.pause_game_clock()

        if params == False:
            params = progression_levels.next()

        self.params = params
        self.sim_speedup = params['sim_speedup']


        self.setup_coord_system(params['simulation_box'])

        # Create Planets
        self.planets = []
        self.planet_pos = []
        for i, pos in enumerate(params['planet_pos']):
            tp = self.transform_pos(pos)
            self.planet_pos.append(tp)
            rad = self.scale_dist(params['planet_radius'][i])
            img = params['planet_img'][i]
            self.planets.append(Planet(radius = rad, pos = tp, img = img))
            self.add_widget(self.planets[-1])

            # Calculate the canon pos
            if i == params['canon_planet']:
                angle = params['canon_planet_angle']
                rad_angle = math.radians(angle)
                x = tp[0] + math.sin(rad_angle) * rad
                y = tp[1] + math.cos(rad_angle) * rad
                self.canon_pos = (x, y)

        self.canon = Canon(pos = self.canon_pos, angle = angle,
            max_angle = params['canon_max_angle'])
        self.add_widget(self.canon)


        # Setup the checkpoints
        self.checkpoints = []
        for i, planet in enumerate(params['checkpoint_planet']):

            # find the start and endpoint of the checkpoint
            angle = math.radians(params['checkpoint_angle'][i])
            vect = [math.sin(angle), math.cos(angle)]
            p_pos = params['planet_pos'][planet]

            points = []
            seg = params['checkpoint_segment'][i]
            seg = [self.scale_dist(s) for s in seg]

            for d in seg:
                p = [p_pos[ii] + d * vect[ii] for ii in range(2)]
                p = self.transform_pos(p)
                points += p

            cp = Checkpoint(points,params['checkpoint_reward'][i])

            self.add_widget(cp)
            self.checkpoints.append(cp)

        # Add Buttons
        self.accelerate_btn = FlatButton(btn_callback = self.btn_press,
            btn_name = 'up', size = (200, 100), pos = (980, 20))

        self.brake_btn = FlatButton(btn_callback = self.btn_press,
            btn_name = 'down', size = (200, 100), pos = (100, 20))

        self.pause_btn = FlatButton(btn_callback = self.btn_press,
            btn_name = 'pause', size = (60, 60), pos = (self.size_win[0] - 80, self.size_win[1] - 80))

        self.add_widget(self.accelerate_btn)
        self.add_widget(self.brake_btn)
        self.add_widget(self.pause_btn)

        # Reward and time display
        h1 = self.size_win[1] - 28
        h2 = self.size_win[1] - 75
        self.time_disp = Label(text = '546.3', font_size=32,
            center = (90, h1))
        self.reward_disp = Label(text = '101', font_size=32,
            center = (90, h2))

        self.time_img = Icon(img = 'img/icons/time.png',
            pos = (15, h1-14), size = (28,28))
        self.reward_img = Icon(img = 'img/icons/kite.png',
            pos = (15, h2-14), size = (28,28))

        self.add_widget(self.reward_disp)
        self.add_widget(self.time_disp)
        self.add_widget(self.time_img)
        self.add_widget(self.reward_img)

        # Add trace
        self.trace = Trace(n_points = 359)
        self.add_widget(self.trace)

        # No kite yet
        self.kite = None

        # Random scheme
        theme = random_sequential()
        self.set_color_theme(theme)

        # This is really needed!
        self.start_launch()

        self.start_game_clock()


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


    def btn_press(self, *args, **kwargs):
        btn_down = args[0].state == 'down'
        btn = args[0].name # This is defined to .text is not neede anymore

        if btn == 'pause' and btn_down:
            self.load_level()
            return

        # Trigger launch
        if self.launching and btn_down:
            self.launch_kite()

        # Control kite
        elif not self.launching:
            # Process user input
            self.kite.user_input(btn, btn_down)


    def launch_kite(self):
        pos, angle = self.canon.launch()

        # Initial velocity in scaled coordinates
        vel = self.params['canon_velocity'] * self.scale_factor
        r = math.radians(angle)
        vect = [vel * math.sin(r), vel * math.cos(r)]

        # Set position and velocity of kite
        p = [pos[0] + vect[0], pos[1] + vect[1]]
        self.kite.pos = (pos[0] + vect[0], pos[1] + vect[1])
        self.kite.velocity = vect

        # End launching sequence, show trace & kite
        self.launching = False
        self.trace.opacity = 1.0
        self.kite.opacity = 1.0


    def start_launch(self):
        '''
            Start launch sequence for new kite:
                1) Reset all episode stats
                2) Start canon aim
                3) Any button triggers launch_kite()
        '''
        # Reset episode data
        self.reward = 0
        self.steps = 0
        self.episode_time = 0
        self.passed_checkpoint = [False for x in self.params['checkpoint_planet']]
        self.time_complete_checkpoints = -1
        self.last_checkpoint = -1

        # Hide trace, reset text display
        self.trace.opacity = 0.0
        self.trace.reset()
        self.time_disp.text = '0'
        self.reward_disp.text = '0'

        # Make all checkpoints active
        for c in self.checkpoints:
            c.active = True

        # Remove kite and make new one
        if self.kite is not None:
            self.remove_widget(self.kite)

        self.kite = Kite(pos = (0,0), velocity=(0,0), acceleration = self.params['acc'])
        self.add_widget(self.kite)
        self.kite.opacity = 0.0

        # Set random theme
        theme = random_sequential()
        self.set_color_theme(theme)

        # We are starting the launch sequence for a new kite
        self.launching = True
        self.paused = False
        self.canon.start_launch()


    def update(self,dt):
        if not self.launching:
            self.episode_time += dt
            # Show the episode time in realtime if not all checkpoints
            if not all(self.passed_checkpoint):
                self.time_disp.text = str(int(self.episode_time))

        # Speed up the simulation a bit
        dt *= self.sim_speedup
        self.steps += 1

        # Move kite if not paused
        remove_kite = False

        if not self.paused and not self.launching:
            # Get gravity vector for kite
            gravity = self.get_gravity_vector(dt)

            # Process user inputs
            self.kite.update(dt)

            # Update velocity
            self.kite.velocity[0] += gravity[0]
            self.kite.velocity[1] += gravity[1]

            # Update Position
            self.kite.pos[0] += dt * self.kite.velocity[0]
            self.kite.pos[1] += dt * self.kite.velocity[1]

            # Collision: Leave screen
            if not 0 < self.kite.pos[0] < self.size_win[0]:
                remove_kite = True

            elif not 0 < self.kite.pos[1] < self.size_win[1]:
                remove_kite = True

            else:
                # Collision detection: planets
                p = tuple(self.kite.pos)
                planet_vect = []
                planet_dist = []
                for j, planet in enumerate(self.planets):
                    vect = [planet.pos[0] - p[0], planet.pos[1] - p[1]]
                    dist = math.hypot(*vect)

                    # No need to scale vector bc its only needed for angle calc
                    planet_vect.append(vect)
                    planet_dist.append(self.scale_dist(dist))

                    if dist < planet.radius:
                        remove_kite = True
                        break

                if not remove_kite:
                    # Collision with checkpoint
                    # Collide widget doesnt work:(
                    pos = self.kite.pos

                    for c, cp in enumerate(self.checkpoints):
                        # Have to take other checkpoint before retaking this one
                        # Also prevents multiple rewards during passage of the checkpoint
                        if not self.last_checkpoint == c:

                            planet_id = self.params['checkpoint_planet'][c]
                            seg = self.params['checkpoint_segment'][c]

                            if seg[0] < planet_dist[planet_id] < seg[1]:
                                v = planet_vect[planet_id]
                                angle = math.degrees(math.atan2(v[1],v[0]))
                                angle = (270-angle)%360

                                if abs(angle - self.params['checkpoint_angle'][c]) < 2.5:
                                    print 'Got checkpoint', c, angle
                                    self.last_checkpoint = c

                                    # Change active checkpoints (color)
                                    for i, check in enumerate(self.checkpoints):
                                        if i == self.last_checkpoint:
                                            check.active = False
                                        else:
                                            check.active = True

                                    # give reward
                                    self.reward += self.params['checkpoint_reward'][c]
                                    self.reward_disp.text = str(self.reward)

                                    # Log checkpoint and check if first time all checkoints
                                    not_all = all(self.passed_checkpoint)
                                    self.passed_checkpoint[c] = True
                                    if all(self.passed_checkpoint) and not not_all:
                                        self.time_disp.text = str(round(self.episode_time, 1))
                                        self.time_complete_checkpoints = self.episode_time
                                        print 'Completed checkpoints', round(self.episode_time,1)
                                    break

            # Remove kite if collided
            if remove_kite:
                self.remove_widget(self.kite)
                self.kite = None

                self.start_launch()

            # Update Trace
            if not self.launching and not self.steps%3:
                pos = self.kite.pos
                self.trace.add_point(pos)


    def get_gravity_vector(self, dt):
        '''
            Calculates vector of gravity for kite
        '''
        vectors = []
        pm = self.params['planet_mass']
        G = self.params['gravity_constant']

        pos = self.kite.pos
        tot_force = [0,0]
        for i, p_pos in enumerate(self.planet_pos):
            vect = (p_pos[0]-pos[0], p_pos[1] - pos[1])
            dist = math.hypot(vect[0], vect[1]) * self.scale_factor
            gravity = G * pm[i] / (dist**2)
            tot_force[0] += dt * vect[0] * gravity / dist
            tot_force[1] += dt * vect[1] * gravity / dist

        return tot_force


    def set_color_theme(self, theme):
        if self.kite is not None:
            self.kite.color_bg = theme['kite_bg']
            self.kite.color_hl = theme['kite_hl']

        for p in self.planets:
            p.color_bg = theme['planet_bg']
            p.color_hl = theme['planet_hl']

        for p in self.checkpoints:
            p.color_bg = theme['checkpoint_bg']
            p.color_hl = theme['checkpoint_hl']

        for btn in [self.accelerate_btn, self.brake_btn, self.pause_btn]:
            btn.color_bg = theme['btn_bg']
            btn.color_hl = theme['btn_hl']

        self.time_img.color_bg = theme['icon_bg']
        self.reward_img.color_bg = theme['icon_bg']
        self.time_disp.color = list(theme['icon_bg']) + [1]
        self.reward_disp.color = list(theme['icon_bg']) + [1]

        self.canon.color_bg = theme['canon_bg']
        self.trace.color_bg = theme['trace_bg']
        self.color_bg = theme['main_bg']


    def transform_pos(self, pos):
        tv = self.transform_vect
        return (pos[0] + tv[0], pos[1] + tv[1])


    def scale_dist(self, dist):
        return dist * self.scale_factor


    def scale_vect(self, vect):
        return (vect[0] * self.scale_factor, vect[1] * self.scale_factor)


    def pause_game_clock(self):
        Clock.unschedule(self.update)


    def start_game_clock(self):
        Clock.schedule_interval(self.update, 1.0/40.0)



if __name__ == '__main__':
    game_display = GameDisplay()