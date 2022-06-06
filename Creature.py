import Map
import Food
import LinkedList

import random as rand
import math as m

t_pi = 2 * m.pi

class Creature:
    """The Creature object that evolves

    Static Parameters
    ------------
    eat_radius: The distance a creature must be from food in order to eat it
    \b
    max_v_theta: The maximum velocity (first derivative) of theta that can be attained each time step
    \b
    max_a_theta: The maximum acceleration (second derivative) of theta that can be attained each time step
    \b
    max_j_theta: The maximum jerk (third derivative) of theta that can be attained each time step
    \b
    max_offset_percent: The maximum variation a creature  has from facing the center

    Instance Parameters
    ------------
    map: The associated map class (must be an instance of Map in order to work properly)
    \b
    radius: the polar coordinate r of the Creature object
    \b
    theta: the polar coordinate theta of the Creature object
    \b
    direction: the polar theta direction of the vector on which the Creature is currently travelling
    \b
    speed: the magnitude of the direction in which the Creature is currently travelling
    \b
    d1_theta: the first derivative of direction. AKA the first derivative of the Creature's travel theta
    \b
    d2_theta: the second derivative of direction. AKA the second derivative of the Creature's travel theta
    \b
    food_eaten: the amount of food the Creature has currently consumed
    \b
    energy_left: The amount of energy the Creature currently has left to move"""

    eat_radius = 0.1
    max_v_theta = m.pi
    max_a_theta = m.pi/8
    max_j_theta = 1.0
    max_offset_percent = 0.15
    base_energy = 10.0

    def __init__(self, map=None, radius=0.0, theta=0.0, direction=0.0, speed=1.5, d1_theta=0.0, d2_theta=0.0, food_eaten=0,
                 energy_left=base_energy):
        self.map = map
        self.radius = radius
        self.theta = theta
        self.direction = direction
        self.d1_theta = d1_theta
        self.d2_theta = d2_theta
        self.speed = speed
        self.food_eaten = food_eaten
        self.energy_left = energy_left

    def creature_reset(self):
        max_offset_percent = self.max_offset_percent
        cur_theta = (t_pi * rand.random()) % t_pi
        cur_offset_percent = (1 + max_offset_percent * (2 * rand.random() - 1))
        cur_direction = (cur_theta + (m.pi * cur_offset_percent)) % t_pi

        self.radius = self.map.map_radius
        self.theta = cur_theta
        self.direction = cur_direction

        self.d1_theta = 0
        self.d2_theta = 0
        self.food_eaten = 0
        self.energy_left = self.base_energy

    def creature_movement(self):
        """A function that returns a boolean. The function will return False if the creature could/did not move and
        True if it did."""
        cur_energy = self.energy_left

        if cur_energy <= 0:
            return False

        time_step = self.map.time_step
        map_radius = self.map.map_radius

        # Third derivative of orientation is random every time step
        this_j_theta = ((2 * rand.random()) - 1) * self.max_j_theta

        cur_radius = self.radius
        cur_theta = self.theta

        start_x, start_y = Map.polar_to_cartesian(cur_radius, cur_theta)

        cur_speed = self.speed
        # Current orientation, first derivative of orientation, and second derivative of orientation, respectively.
        cur_o_theta = self.direction
        cur_v_theta = self.d1_theta
        cur_a_theta = self.d2_theta

        max_a_theta = self.max_a_theta
        max_v_theta = self.max_v_theta

        cur_a_theta += time_step * this_j_theta
        if abs(cur_a_theta) > max_a_theta:
            cur_a_theta = max_a_theta * cur_a_theta/abs(cur_a_theta)

        cur_v_theta += time_step * cur_a_theta + (1 / 2) * (time_step ** 2) * this_j_theta
        if abs(cur_v_theta) > max_v_theta:
            cur_v_theta = max_v_theta * cur_v_theta/abs(cur_v_theta)

        cur_o_theta += (time_step * cur_v_theta + (1 / 2) * (time_step ** 2) * cur_a_theta + (1 / 6) * (
                    time_step ** 3) * this_j_theta) % t_pi

        d_x, d_y = Map.polar_to_cartesian((cur_speed * time_step), cur_o_theta)
        end_r, end_theta = Map.cartesian_to_polar((start_x + d_x), (start_y + d_y))

        cur_energy -= time_step * (cur_speed ** 2)
        if end_r >= map_radius or cur_energy <= 0:
            cur_energy = 0

        self.radius = end_r
        self.theta = end_theta
        self.direction = cur_o_theta
        self.d1_theta = cur_v_theta
        self.d2_theta = cur_a_theta
        self.energy_left = cur_energy
        return False if cur_energy == 0 else True

    def distance_checker(self, this_food):
        """Returns true if the creature and food are in range of each other."""
        if (abs(self.radius - this_food.radius) <= self.eat_radius) and (
                abs(self.theta - this_food.theta) <= this_food.theta_lim):
            r1 = self.radius
            r2 = this_food.radius

            t1 = self.theta
            t2 = this_food.theta

            x1, y1 = Map.polar_to_cartesian(r1, t1)
            x2, y2 = Map.polar_to_cartesian(r2, t2)

            d = m.sqrt((x1-x2)**2 + (y1-y2)**2)

            if d <= self.eat_radius:
                return True
        return False

    def creature_eat_handler(self, this_food):
        r1 = self.radius
        r2 = this_food.radius

        t1 = self.theta
        t2 = this_food.theta

        x1, y1 = Map.polar_to_cartesian(r1, t1)
        x2, y2 = Map.polar_to_cartesian(r2, t2)

        d = m.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if d <= self.eat_radius:
            self.food_eaten += 1
            return True

        return False

    def copy(self):
        return Creature(self.map, self.radius, self.theta, self.direction, self.speed, self.d1_theta, self.d2_theta,
                        self.food_eaten, self.energy_left)
