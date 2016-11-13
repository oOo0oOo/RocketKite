import math
import random

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
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
        self.accelerate_btn = Button(text = 'down', size = (150, 100), font_size = 12,
            background_color = [1.0]*3+[0.7],
            pos = (900, 20), on_press = self.btn_press, on_release = self.btn_press)

        self.brake_btn = Button(text = 'up', size = (150, 100), font_size = 12,
            background_color = [1.0]*3+[0.7],
            pos = (1075, 20), on_press = self.btn_press, on_release = self.btn_press)

        self.left_btn = Button(text = 'left', size = (150, 100), font_size = 12,
            background_color = [1.0]*3+[0.7],
            pos = (100, 20), on_press = self.btn_press, on_release = self.btn_press)

        self.right_btn = Button(text = 'right', size = (150, 100), font_size = 12,
            background_color = [1.0]*3+[0.7],
            pos = (275, 20), on_press = self.btn_press, on_release = self.btn_press)

        self.reset_btn = Button(text = 'reset', size = (60, 60), font_size = 0,
            background_color = [1.0]*3+[0.7],
            pos = (20, self.size_win[1] - 80), on_press = self.btn_press)

        self.add_widget(self.accelerate_btn)
        self.add_widget(self.brake_btn)
        self.add_widget(self.left_btn)
        self.add_widget(self.right_btn)
        self.add_widget(self.reset_btn)

        # Reward and time display
        self.reward_disp = Label(text = '101', font_size=38,
            center = (150, 680))
        self.time_disp = Label(text = '546.3', font_size=32,
            center = (900, 680))
        self.add_widget(self.reward_disp)
        self.add_widget(self.time_disp)

        # Add trace
        self.trace = Trace(n_points = 359)
        self.add_widget(self.trace)

        # No spaceships yet
        self.spaceships = []
        self.control = -1

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
        btn = args[0].text

        if btn == 'reset' and btn_down:
            self.load_level()
            return

        # Trigger launch
        if self.launching and btn_down:
            self.launch_spaceship()

        # Control spaceship
        if self.control > -1:
            # Process user input
            self.spaceships[self.control].user_input(btn, btn_down)

            # Accelerate if up
            # if btn == 'up':
            #     self.spaceships[self.control].accelerate = btn_down

            # if btn == 'down':
            #     self.spaceships[self.control].accelerate = btn_down

            # elif btn in ('left', 'right'):
            #     if not btn_down:
            #         self.spaceships[self.control].turn = 0

            #     elif btn == 'left':
            #         self.spaceships[self.control].turn = -1

            #     elif btn == 'right':
            #         self.spaceships[self.control].turn = 1


    def launch_spaceship(self):
        pos, angle = self.canon.launch()

        # Initial velocity in scaled coordinates
        vel = self.params['canon_velocity'] * self.scale_factor
        r = math.radians(angle)
        vect = [vel * math.sin(r), vel * math.cos(r)]

        # Create a new SpaceShip
        pos = [pos[0] + vect[0], pos[1] + vect[1]]
        spaceship = SpaceShip(pos = pos, velocity=vect, acceleration = self.params['acc'])

        self.add_widget(spaceship)
        self.spaceships.append(spaceship)

        # And control it
        self.control = len(self.spaceships) - 1
        self.launching = False

        # Enable trace
        self.trace.opacity = 1.0

        # Set a new theme
        theme = random_sequential()
        self.set_color_theme(theme)


    def start_launch(self):
        self.canon.start_launch()
        self.launching = True
        self.control = -1
        self.trace.opacity = 0.0
        self.last_checkpoint = -1
        self.trace.reset()
        self.reward = 0
        self.passed_checkpoint = [False for x in self.params['checkpoint_planet']]
        self.steps = 0
        self.paused = False
        self.episode_time = 0
        self.time_complete_checkpoints = -1

        self.time_disp.text = '0'
        self.reward_disp.text = '0'


    def update(self,dt):
        if not self.launching:
            self.episode_time += dt
            # Show the episode time in realtime if not all checkpoints
            if not all(self.passed_checkpoint):
                self.time_disp.text = str(int(self.episode_time))

        # Speed up the simulation a bit
        dt *= self.sim_speedup
        self.steps += 1

        # Move all spaceships if not paused
        if not self.paused:
            # Get gravity vector for all spaceships
            gravity = self.get_gravity_vectors(dt)

            # Update each spaceship
            to_remove = []
            for i, spaceship in enumerate(self.spaceships):
                # Process user inputs
                spaceship.update(dt)

                # Update velocity
                spaceship.velocity[0] += gravity[i][0]
                spaceship.velocity[1] += gravity[i][1]

                # Update Position
                spaceship.pos[0] += dt * spaceship.velocity[0]
                spaceship.pos[1] += dt * spaceship.velocity[1]

                # Collision: Leave screen
                if not 0 < spaceship.pos[0] < self.size_win[0]:
                    to_remove.append(i)
                elif not 0 < spaceship.pos[1] < self.size_win[1]:
                    to_remove.append(i)

                # Collision detection: planets
                for j, p in enumerate(self.planets):
                    vect = [p.pos[0] - spaceship.pos[0], p.pos[1] - spaceship.pos[1]]
                    dist = math.hypot(*vect)
                    if dist < p.radius:
                        to_remove.append(i)
                        break

                # Collision with other spaceships
                for k in range(i+1, len(self.spaceships)):
                    vect = [self.spaceships[k].pos[jjj] - spaceship.pos[jjj] for jjj in range(2)]
                    dist = math.hypot(*vect)
                    if dist < 15:
                        to_remove.append(k)
                        to_remove.append(i)


                # Collision with checkpoint
                # Collide widget doesnt work:(
                pos = spaceship.pos

                for c, cp in enumerate(self.checkpoints):
                    if not self.last_checkpoint == c:
                        p_pos = self.planet_pos[self.params['checkpoint_planet'][c]]

                        # Convert to polar coords around planet
                        x = pos[0] - p_pos[0]
                        y = pos[1] - p_pos[1]

                        dist = math.hypot(x,y)
                        seg = self.params['checkpoint_segment'][c]

                        if seg[0] < dist < seg[1]:
                            angle = math.degrees(math.atan2(y,x))
                            angle = (90-angle)%360
                            if abs(angle - self.params['checkpoint_angle'][c]) < 2.5:
                                self.last_checkpoint = c

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


            # Remove collided spaceships
            for i in reversed(sorted(set(to_remove))):
                self.remove_widget(self.spaceships[i])
                del self.spaceships[i]

                # The one under control was destroyed
                if i == self.control:
                    self.control = -1
                    self.start_launch()

            # Update Trace
            if self.control != -1 and not self.steps%3:
                pos = self.spaceships[self.control].pos
                self.trace.add_point(pos)


    def get_gravity_vectors(self, dt):
        '''
            Calculates vector of gravity for all spaceships
        '''
        vectors = []
        pm = self.params['planet_mass']
        G = self.params['gravity_constant']

        for j, spaceship in enumerate(self.spaceships):
            pos = spaceship.pos
            tot_force = [0,0]
            for i, p_pos in enumerate(self.planet_pos):
                vect = (p_pos[0]-pos[0], p_pos[1] - pos[1])
                dist = math.hypot(vect[0], vect[1]) * self.scale_factor
                gravity = G * pm[i] / (dist**2)
                tot_force[0] += dt * vect[0] * gravity / dist
                tot_force[1] += dt * vect[1] * gravity / dist
            vectors.append(tot_force)
        return vectors


    def set_color_theme(self, theme):
        if len(self.spaceships) > 0:
            self.spaceships[-1].color_bg = theme['kite_bg']
            self.spaceships[-1].color_hl = theme['kite_hl']

        for p in self.planets:
            p.color_bg = theme['planet_bg']
            p.color_hl = theme['planet_hl']

        for p in self.checkpoints:
            p.color_bg = theme['checkpoint_bg']

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