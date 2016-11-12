from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.animation import Animation

import math
import random

planets = ['Venus', 'Earth', 'Mars', 'Jupiter', 'Neptune', 'Pluto']

class Planet(Widget):
    radius = NumericProperty(2)
    img = StringProperty('')

    def __init__(self, radius = 2, **kwargs):
        super(Planet, self).__init__(**kwargs)
        self.radius = radius
        self.img = 'img/planets/{}.png'.format(random.choice(planets))

class Canon(Widget):
    angle = NumericProperty(0)
    def __init__(self, angle = 0, max_angle = 10, **kwargs):
        super(Canon, self).__init__(**kwargs)
        self.angle = angle
        self.max_angle = max_angle

        # The aim movement of the canon
        t = 0.5
        anim = Animation(angle = angle-max_angle, d = t)
        anim += Animation(angle = angle+max_angle, d = 2*t)
        anim += Animation(angle = angle, d = t)
        anim.repeat = True

        self.anim = anim


    def start_launch(self):
        self.opacity = 1.0
        # Animate the angle of the canon
        self.anim.start(self)


    def launch(self):
        # Return position and angle
        angle = float(self.angle)
        self.anim.cancel(self)
        self.opacity = 0.0
        return self.pos, angle


class PredictionSign(Widget):
    def __init__(self, **kwargs):
        super(PredictionSign, self).__init__(**kwargs)


class Prediction(Widget):
    def __init__(self, n_points = 5, **kwargs):
        super(Prediction, self).__init__(**kwargs)
        self.n_points = n_points
        self.points = [PredictionSign() for p in range(n_points)]
        [self.add_widget(p) for p in self.points]


    def set_points(self, positions):
        for p, pos in zip(self.points, positions):
            p.pos = pos


class Trace(Widget):
    points = ListProperty([])
    def __init__(self, n_points = 100, **kwargs):
        super(Trace, self).__init__(**kwargs)
        self.n_points = n_points
        self.points = []

    def add_point(self, pos):
        # pos = tuple(pos)
        self.points.append(pos[0])
        self.points.append(pos[1])
        if len(self.points) > self.n_points * 2:
            self.points = self.points[2:]

    def reset(self):
        self.points = []


class SpaceShip(Widget):
    angle = NumericProperty(0)
    def __init__(self, pos = (0,0), velocity = [10,10], angle = 0,
        acceleration = 0, acc_ang = 0, **kwargs):

        super(SpaceShip, self).__init__(**kwargs)
        self.angle = angle
        self.velocity = velocity
        self.pos = pos
        self.acc = acceleration
        self.acc_ang = acc_ang

        self.accelerate = False
        self.turn = 0 # -1, 0, 1 (clockwise)

        assert type(velocity) == list


    def update(self, dt):
        # Boost
        if self.accelerate:
            abs_angle = math.radians((360+self.angle)%360)
            self.velocity[0] += math.sin(abs_angle) * dt * self.acc
            self.velocity[1] += math.cos(abs_angle) * dt * self.acc

        # Turn
        if self.turn in (-1, 1):
            self.angle += 360 + (self.turn * dt * self.acc_ang)
            self.angle %= 360
