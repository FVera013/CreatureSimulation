import Creature
import Food
import LinkedList

import math as m

t_pi = 2 * m.pi


class Map:
    """The Map where Creatures and Food exist

        Static Parameters
        ------------

        Instance Parameters
        ------------
        map_radius: The radius of the circular map
        \b
        food_radius: The distance from the center in which food is allowed to spawn
        \b
        time_step: The amount of time that passes each time creatures move
        \b
        initial_creatures_count: The number of creatures there should be on the map instantiation
        \b
        initial_food_amount: The amount of food there should be on the map on instantiation
        \b
        total_days: The total number of days the simulation should run for
        \b
        creature_children: A child class (must be an instance of DLinkedList containing creature objects in order to
        work properly)
        \b
        food_children: A child class (must be an instance of DLinkedList containing food objects in order to
        work properly)"""

    def __int__(self, map_radius, food_radius, time_step, initial_creatures_count, initial_food_amount, total_days):
        self.map_radius = map_radius
        self.food_radius = food_radius
        self.time_step = time_step
        self.initial_creatures_count = initial_creatures_count
        self.initial_food_amount = initial_food_amount
        self.total_days = total_days
        self.creature_children = None
        self.food_children = None


def polar_to_cartesian(r, theta):
    cart_x = r * m.cos(theta)
    cart_y = r * m.sin(theta)

    return cart_x, cart_y


def cartesian_to_polar(cart_x, cart_y):
    r = m.sqrt(cart_x ** 2 + cart_y ** 2)

    theta = 0 if r == 0 else -1
    quadrant = 1
    if theta == -1:
        if (cart_x <= 0) and (cart_y > 0): quadrant = 2
        if (cart_x < 0) and (cart_y <= 0): quadrant = 3
        if (cart_x >= 0) and (cart_y < 0): quadrant = 4
        if (cart_x == 0) or (cart_y == 0): theta = (quadrant - 1) * (m.pi / 2)
        if theta != -1:
            theta = ((quadrant - 1) * (m.pi / 2)) + m.atan(abs((cart_y / cart_x) ** ((-1) ** (quadrant - 1))))

        theta = theta % t_pi

    return r, theta
