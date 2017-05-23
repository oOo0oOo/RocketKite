from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button
# from kivy.animation import Animation
# from kivy.clock import Clock

import math
import random
from collections import deque


class Planet(Widget):
    radius = NumericProperty(2)
    angle = NumericProperty(0)
    img_bg = StringProperty('')
    img_hl = StringProperty('')
    color_bg = ListProperty([0.5,0.5,0.5])
    color_hl = ListProperty([0.5,0.5,0.5])

    def __init__(self, radius = 2, img = 'mountain1', **kwargs):
        super(Planet, self).__init__(**kwargs)
        self.radius = radius

        self.img_bg = 'img/planets/' + img + '_bg.png'
        self.img_hl = 'img/planets/' + img + '_hl.png'


        self.rotation_period = 10 + 10 * random.random() # s
        self.rotation_period *= random.choice([1, -1])

        self.anim_running = False


    def update(self, dt):
        if self.anim_running:
            self.angle += dt * self.rotation_period


    def stop_rotation(self):
        if self.anim_running:
            self.anim_running = False


    def start_rotation(self):
        self.anim_running = True


class Canon(Widget):
    scale = NumericProperty(1.0)
    angle = NumericProperty(0)
    color_bg = ListProperty([0.5,0.5,0.5])

    def __init__(self, angle = 0, max_angle = 10, planet_angle_delta = 0, scale = 1.0, **kwargs):
        super(Canon, self).__init__(**kwargs)
        self.angle = angle
        self.max_angle = max_angle
        self.scale = scale
        self.center_angle = float(angle)
        self.center_angle += planet_angle_delta

        self.anim_running = False


    def start_launch(self):
        '''
            Starts animation
        '''
        self.opacity = 1.0

        # Set angle in middle
        self.angle = self.center_angle

        # Start in a random direction
        self.delta_angle = random.choice([185., -185.]) # degrees / s

        self.anim_running = True


    def update(self, dt):
        if self.anim_running:

            # Rotate back
            angle_diff = self.angle - self.center_angle

            if angle_diff > self.max_angle:
                self.angle = self.center_angle + self.max_angle
                self.delta_angle *= -1

            elif angle_diff < -self.max_angle:
                self.angle = self.center_angle - self.max_angle
                self.delta_angle *= -1



            self.angle += dt * self.delta_angle



    def launch(self):
        '''
            Stops animation and returns initial pos and angle of kite
        '''
        # Return position and angle
        angle = float(self.angle)
        self.opacity = 0.0
        self.anim_running = False
        return self.pos, angle


class Tail(Widget):
    angle = NumericProperty(0)
    color_bg = ListProperty([0.5,0.5,0.5])
    scale = NumericProperty(1.0)


class Triangles(Widget):
    angle = NumericProperty(0)
    scale = NumericProperty(1.0)
    color_bg = ListProperty([0.5,0.5,0.5])
    color_hl = ListProperty([0.3,0.3,0.3])

    def __init__(self, scale = 1.0, **kwargs):
        super(Triangles, self).__init__(**kwargs)
        self.scale = scale


class Prediction(Widget):
    def __init__(self, n_points = 8, scale = 1.0, **kwargs):
        super(Prediction, self).__init__(**kwargs)
        self.scale = scale
        self.n_points = n_points

        # Create the points
        self.points = []
        for i in range(n_points):
            self.points.append(Tail())
            self.points[-1].scale = self.scale * 0.5
            self.points[-1].opacity = 1. - float(i)/n_points
            self.add_widget(self.points[-1])

    def update_points(self, points = [], angles = []):
        i = 0
        for i, p, point, angle in zip(range(len(points)), self.points, points, angles):
            p.pos = point
            p.angle = angle

        for j in range(i,self.n_points):
            self.points[j].pos = [-100,-100]


class Trace(Widget):
    points = ListProperty([])
    color_bg = ListProperty([0.5,0.5,0.5])
    scale = NumericProperty(1.0)

    def __init__(self, n_points = 55, line_delay = 4, scale = 1.0, **kwargs):
        super(Trace, self).__init__(**kwargs)
        self.n_points = n_points
        self.line_delay = line_delay
        self.scale = scale

        # This is for us to keep track
        self.n_tot = self.n_points * self.line_delay
        self.position = deque()
        self.angles = deque()

        # Add tail
        self.tail = Tail()
        self.tail.scale = scale
        self.add_widget(self.tail)

        # Add triangles
        triangle_scale = [0.65,0.5,0.4]
        triangle_delay = 26
        self.n_triangles = len(triangle_scale)
        self.triangle_inds = [38 + i*triangle_delay for i in range(self.n_triangles)]

        self.triangles = []
        for s in triangle_scale:
            self.triangles.append(Triangles(scale = self.scale * s))
            self.add_widget(self.triangles[-1])

        self.reset()


    def add_point(self, pos, angle):
        pos = tuple(pos)
        angle = float(angle)

        # Add position and velocity
        self.position.appendleft(pos)
        self.angles.appendleft(angle)

        n_pos = len(self.position)
        full_queue = n_pos >= self.n_tot

        # First point
        if n_pos == 1:
            self.tail.opacity = 1.0
            self.tail.pos = pos
            self.tail.angle = angle

        else:
            # Update tail
            if full_queue:
                self.tail.pos = self.position.pop()
                self.tail.angle = self.angles.pop()

            # Update all triangles
            if full_queue:
                available = self.triangle_inds
            else:
                available = [j for j in self.triangle_inds if j <= n_pos]

            for i, t_ind in enumerate(available):
                t_ind -= 2
                self.triangles[i].pos = self.position[t_ind]
                self.triangles[i].angle = self.angles[t_ind]

        # We update the line with subsampling
        if not self.steps%self.line_delay:
            if full_queue:
                self.points = self.points[2:] + list(pos)
            else:
                self.points = self.points + list(pos)

        self.steps += 1


    def reset(self):
        self.points = []
        self.steps = 0

        self.angles.clear()
        self.position.clear()

        self.tail.opacity = 0.0

        for t in self.triangles:
            t.pos = (-1000,-1000)


class Kite(Widget):
    velocity = ListProperty([10,10])
    color_bg = ListProperty([0.5,0.5,0.5])
    color_hl = ListProperty([0.5,0.5,0.5])
    color_rocket = ListProperty([0.5,0.5,0.5])
    color_thrust = ListProperty([1,1,1])

    opacity_backward = NumericProperty(0.0)
    opacity_forward = NumericProperty(0.0)
    scale = NumericProperty(1.0)

    def __init__(self, scale = 1.0, **kwargs):
        super(Kite, self).__init__(**kwargs)
        self.velocity = kwargs['velocity']
        self.pos = kwargs['pos']
        self.acc = kwargs['acceleration']
        self.scale = scale

        self.active_boosters = {i:False for i in ['up', 'down']}
        self.dir_angles = {'up': 0, 'down': 180}


    def user_input(self, btn, btn_down):
        if btn == 'up':
            if btn_down:
                self.opacity_backward = 1.0
            else:
                self.opacity_backward = 0.0

        elif btn == 'down':
            if btn_down:
                self.opacity_forward = 1.0
            else:
                self.opacity_forward = 0.0

        else:
            return

        self.active_boosters[btn] = btn_down


    def get_angle_rev(self):
        angle = math.atan2(float(self.velocity[1]),self.velocity[0])
        angle = (270 + math.degrees(angle))%360
        return angle


    def get_angle(self):
        '''
            0 is north, 90 is east (right)
            This is a variant of the formula used in .kv: 0 is north, 90 is west
                (270 + angle...)
        '''
        angle = math.atan2(float(self.velocity[1]),self.velocity[0])
        angle = (90 - math.degrees(angle))%360

        return angle


    def update(self, dt):
        '''
            Handles the thrusters activated through user input
        '''
        # Angle is forward angle
        abs_angle = self.get_angle()

        # Calculate thrust vector
        vel = [0,0]
        for t, act in self.active_boosters.items():
            if act:
                a = self.dir_angles[t]
                angle = math.radians(abs_angle + a)
                vel[0] += math.sin(angle) * dt * self.acc
                vel[1] += math.cos(angle) * dt * self.acc

        self.velocity[0] += vel[0]
        self.velocity[1] += vel[1]


class Checkpoint(Widget):
    points = ListProperty([])
    color_bg = ListProperty([0.5,0.5,0.5])
    color_hl = ListProperty([0.5,0.5,0.5])
    active = BooleanProperty(True)
    scale = NumericProperty(1.0)

    def __init__(self, points, scale = 1.0, **kwargs):
        super(Checkpoint, self).__init__(**kwargs)
        self.points = points
        self.scale = scale
        self.active = True
        self.active_state = True

        # This also serves as anim_running
        self.blinks_left = 0
        self.delta_opacity = -3.


    def set_active(self, is_active):
        self.active_state = is_active


    def update(self, dt):
        # Blink until there are no blinks left
        if self.blinks_left > 0:
            self.opacity += dt * self.delta_opacity

            if self.opacity <= 0:
                self.delta_opacity *= -1
                self.opacity = 0.0

                # Put correct color before last fade in
                if self.blinks_left == 1:
                    self.active = self.active_state

            elif self.opacity >= 1.0:
                self.delta_opacity *= -1
                self.opacity = 1.0
                self.blinks_left -= 1 # We end on high

        # Otherwise update the state
        elif self.active != self.active_state:
            self.active = self.active_state


    def start_blinking(self, n_blinks = 3):
        self.blinks_left = n_blinks
        self.active = False # Take the not active color


class Icon(Widget):
    color_bg = ListProperty([0.1,0.1,0.1])
    img = StringProperty('')

    def __init__(self, img = '', **kwargs):
        super(Icon, self).__init__(**kwargs)
        self.img = img


class FlatButton(Widget):
    color_bg = ListProperty([0.1,0.1,0.1])
    color_hl = ListProperty([0.8,0.8,0.8])
    btn_img = StringProperty('')
    is_down = BooleanProperty(False)

    def __init__(self, btn_callback, btn_name = '', btn_img = '', **kwargs):
        super(FlatButton, self).__init__(**kwargs)
        self.btn_callback = btn_callback

        self.btn = Button(on_press = self.update_down,
            on_release = self.update_down, **kwargs)
        self.btn.name = btn_name
        self.btn_img = btn_img

        self.btn.background_color = 1,1,1
        self.btn.background_normal = ''
        self.btn.background_down = ''

        self.add_widget(self.btn)

    def update_down(self, *args):
        '''
            This method is used because the button sometimes doesnt trigger a release event.
            Empirically this happens when the btn press is very short.
            Thus schedule_once a shortly after the btn press should be enough. ?
        '''
        if not self.is_down and self.btn.state == 'down':
            self.is_down = True
            self.btn_callback(self.btn)

        elif self.is_down and self.btn.state != 'down':
            self.is_down = False
            self.btn_callback(self.btn)


class AnimFlatButton(FlatButton):
    def __init__(self, *args, **kwargs):
        super(AnimFlatButton, self).__init__(*args, **kwargs)

        # Blinking animation
        self.blinking_delay = 0.8
        self.anim_running = False
        self.t_since_last = 0.0


    def toggle_down(self, *args):
        self.is_down = not self.is_down


    def update(self, dt):
        if self.anim_running:
            self.t_since_last += dt
            if self.t_since_last >= self.blinking_delay:
                self.toggle_down()
                self.t_since_last = 0.0


    def start_animation(self):
        if not self.anim_running:
            self.anim_running = True
            self.t_since_last = self.blinking_delay


    def stop_animation(self):
        if self.anim_running:
            self.anim_running = False