class Creature:
    """The Creature object that evolves

    Parameters
    ------------
    radius: the polar coordinate r of the Creature object
    theta: the polar coordinate theta of the Creature object
    direction: the polar theta direction of the vector on which the Creature is currently travelling
    speed: the magnitude of the direction in which the Creature is currently travelling
    d1_theta: the first derivative of direction. AKA the first derivative of the Creature's travel theta
    d2_theta: the second derivative of direction. AKA the second derivative of the Creature's travel theta
    food_eaten: the amount of food the Creature has currently consumed
    energy_left: The amount of energy the Creature currently has left ot move"""
    def __init__(self, radius, theta, direction, speed=1, d1_theta=0, d2_theta=0, food_eaten=0, energy_left=10):
        self.radius = radius
        self.theta = theta
        self.direction = direction
        self.d1_theta = d1_theta
        self.d2_theta = d2_theta
        self.speed = speed
        self.food_eaten = food_eaten
        self.energy_left = energy_left

def creature_reset(this_creature):
    cur_theta = (t_pi * rand.random()) % t_pi
    cur_offset_percent = (1 + max_offset_percent * (2 * rand.random() - 1))
    cur_direction = ((cur_theta + m.pi) * cur_offset_percent) % t_pi

    setattr(this_creature, 'radius', map_radius)
    setattr(this_creature, 'theta', cur_theta)
    setattr(this_creature, 'direction', cur_direction)

    setattr(this_creature, 'd1_theta', 0)
    setattr(this_creature, 'd2_theta', 0)
    setattr(this_creature, 'food_eaten', 0)
    setattr(this_creature, 'energy_left', 10)
