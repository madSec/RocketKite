from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.animation import Animation

import math
import random


class Planet(Widget):
    radius = NumericProperty(2)
    img_bg = StringProperty('')
    img_hl = StringProperty('')
    color_bg = ListProperty([0.5,0.5,0.5])
    color_hl = ListProperty([0.5,0.5,0.5])

    def __init__(self, radius = 2, img = 'mountain1', **kwargs):
        super(Planet, self).__init__(**kwargs)
        self.radius = radius

        self.img_bg = 'img/planets/' + img + '_bg.png'
        self.img_hl = 'img/planets/' + img + '_hl.png'


class Canon(Widget):
    angle = NumericProperty(0)
    color_bg = ListProperty([0.5,0.5,0.5])

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


class Trace(Widget):
    points = ListProperty([])
    color_bg = ListProperty([0.5,0.5,0.5])

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


class Kite(Widget):
    velocity = ListProperty([10,10])
    color_bg = ListProperty([0.5,0.5,0.5])
    color_hl = ListProperty([0.5,0.5,0.5])

    def __init__(self, **kwargs):
        super(Kite, self).__init__(**kwargs)
        self.velocity = kwargs['velocity']
        self.pos = kwargs['pos']
        self.acc = kwargs['acceleration']

        self.active_boosters = {i:False for i in ['up', 'down']}
        self.dir_angles = {'up': 0, 'down': 180}


    def user_input(self, btn, btn_down):
        self.active_boosters[btn] = btn_down


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

    def __init__(self, points, reward, **kwargs):
        super(Checkpoint, self).__init__(**kwargs)
        self.points = points
        self.reward = reward
        self.active = True