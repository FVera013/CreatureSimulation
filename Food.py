import Creature

import random as rand
import math as m

t_pi = 2 * m.pi

class Food:
    """The Food object that creatures can consume

    Static Parameters
    ------------

    Instance Parameters
    ------------
    map: The associated map class (must be an instance of Map in order to work properly)
    \b
    radius: the polar coordinate r of the Food object
    \b
    theta: the polar coordinate theta of the Food object
    \b
    theta_lim: how close the creature theta must be in order for consumption"""

    def __init__(self, map=None, radius=0.0, theta=0.0, theta_lim=0.0):
        self.map = map
        self.radius = radius
        self.theta = theta
        self.theta_lim = theta_lim

    def food_reset(self):
        eat_radius = Creature.Creature.eat_radius
        cur_radius = self.map.food_radius * rand.random()
        cur_theta = (t_pi * rand.random()) % t_pi
        cur_theta_lime = m.atan(eat_radius / cur_radius)

        self.radius = cur_radius
        self.theta = cur_theta
        self.theta_lim = cur_theta_lime
