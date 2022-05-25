import copy
import random as rand
import math as m

t_pi = 2 * m.pi

initial_creatures_count = 10
initial_food_amount = 500
total_days = 1000
eat_radius = 0.1

#defines the max jerk_theta, third derivative of theta, the creature can achieve
max_j_theta = 1

#max percent
max_offset_percent = 0.05
map_radius = 15.0
food_radius = 6.0
time_step = 0.01
total_time_steps_per_day = time_step

class Creature:
    def __init__(self, radius, theta, direction, speed=1, d1_theta=0, d2_theta=0, food_eaten=0, energy_left=10):
        self.radius = radius
        self.theta = theta
        self.direction = direction
        self.d1_theta = d1_theta
        self.d2_theta = d2_theta
        self.speed = speed
        self.food_eaten = food_eaten
        self.energy_left = energy_left


class Food:
    def __init__(self, radius, theta, theta_lim):
        self.radius = radius
        self.theta = theta
        self.theta_lim = theta_lim

def polar_to_cartesian(r, theta):
    cart_x = r * m.cos(theta)
    cart_y = r * m.sin(theta)

    return cart_x, cart_y

def cartesian_to_polar(cart_x, cart_y):
    r = m.sqrt(cart_x**2 + cart_y**2)

    theta = 0 if r == 0 else -1
    quadrant = 1
    if theta == -1:
        if cart_x<=0 and cart_y>0: quadrant = 2
        if cart_x<0 and cart_y<=0: quadrant = 3
        if cart_x<=0 and cart_y<0: quadrant = 4
        if cart_x==0 or cart_y==0: theta = (quadrant-1) * (m.pi/2)
        if theta!=-1: theta = ((quadrant-1) * (m.pi/2)) + m.arctan( abs( (cart_y/cart_x) ** ((-1)**(quadrant-1)) ) )
        theta = theta % t_pi

    return r, theta

def position_checker(this_creature):
    if this_creature.radius > map_radius:
        setattr(this_creature, 'energy_left', 0)

def creature_movement(this_creature):
    this_j_theta = (rand.random()*2 - 1) * max_j_theta

    cur_radius = this_creature.radius
    cur_speed = this_creature.speed
    cur_theta = this_creature.theta
    cur_energy = this_creature.energy_left

    start_x, start_y = polar_to_cartesian(cur_radius, cur_theta)

    cur_v_theta = this_creature.d1_theta
    cur_a_theta = this_creature.d2_theta

    cur_a_theta += time_step*this_j_theta
    cur_v_theta += time_step*cur_a_theta + (1/2)*(time_step**2)*this_j_theta
    cur_theta += time_step*cur_v_theta + (1/2)*(time_step**2)*cur_a_theta + (1/6)*(time_step**3)*this_j_theta

    d_x, d_y = polar_to_cartesian(cur_speed*time_step, cur_theta)
    end_r, end_theta = cartesian_to_polar(start_x + d_x, start_y + d_y)

    if end_r >= map_radius or cur_energy <= 0:
        cur_energy = 0

    elif end_r < map_radius and cur_energy > 0:
        cur_energy -= time_step * cur_speed

    setattr(this_creature, 'radius', end_r)
    setattr(this_creature, 'theta', end_theta)
    setattr(this_creature, 'd1_theta', cur_v_theta)
    setattr(this_creature, 'd2_theta', cur_a_theta)
    setattr(this_creature, 'energy_left', cur_energy)

def distance_checker(this_creature, this_food):
    """Returns true if the creature and food are in range of each other."""
    if (abs(this_creature.radius - this_food.radius) <= eat_radius) and (
            abs(this_creature.theta - this_food.theta) <= this_food.theta_lim):
        r1 = this_creature.radius
        r2 = this_food.radius

        t1 = this_creature.theta
        t2 = this_food.theta

        d = m.sqrt(r1*r1 + r2*r2 - 2*r1*r2 * m.cos(t1 - t2))

        if d <= eat_radius:
            return True
    return False

def creature_eat_handler(this_creature, this_food):
    if distance_checker(this_creature, this_food):
        setattr(this_creature, 'food_eaten', this_creature.food_eaten + 1)
        return True

    return False

def creature_next_generation_handler(this_creature, cur_list_index, cur_day_index):
    this_food_eaten = this_creature.food_eaten
    this_list_index = cur_list_index

    if this_food_eaten == 0:
        dead_creatures_list[cur_day_index].append(this_creature)
        return True
    elif this_food_eaten == 1:
        creature_reset(this_creature)
        living_creatures_list[this_list_index].append(this_creature)
        return True
    elif this_food_eaten > 1:
        creature_reset(this_creature)
        child_creature = copy.deepcopy(this_creature)
        living_creatures_list[this_list_index].append(this_creature)
        living_creatures_list[this_list_index].append(child_creature)
        return True
    return False

def creature_reset(this_creature):
    cur_theta = t_pi * rand.random()
    cur_offset_percent = (1 + max_offset_percent * (2 * rand.random() - 1))
    cur_direction = ((cur_theta + m.pi) * cur_offset_percent) % t_pi

    setattr(this_creature, 'radius', map_radius)
    setattr(this_creature, 'theta', cur_theta)
    setattr(this_creature, 'direction', cur_direction)

    setattr(this_creature, 'd1_theta', 0)
    setattr(this_creature, 'd2_theta', 0)
    setattr(this_creature, 'food_eaten', 0)
    setattr(this_creature, 'energy_left', 10)


old_creatures_list = []

for each in initial_creatures_count:
    cur_theta = t_pi * rand.random()
    cur_offset_percent = (1 + max_offset_percent * (2 * rand.random() - 1))
    cur_direction = ((cur_theta + m.pi) * cur_offset_percent) % t_pi
    old_creatures_list.append(Creature(map_radius, cur_theta, cur_direction))

dead_creatures_list = []
for day in range(total_days):
    dead_creatures_list.append([])

living_creatures_list = [old_creatures_list.copy(), []]
final_creatures_list = []

food_list = []
for all in initial_food_amount:
    cur_radius = food_radius * rand.random()
    food_list.append(Food(cur_radius, t_pi * rand.random(), m.asin(eat_radius / cur_radius)))

########################################################################################################################
########################################################################################################################

#Need to repeat this for every day
for day in range(total_days):
    creature_list_index = 0
    cur_creatures_list = living_creatures_list[creature_list_index]
    creatures_moving = len(cur_creatures_list)

    #While loop instead of a for loop, because it makes handling simpler
    while creatures_moving > 0:
        #Move each creature in order
        for cur_creature in cur_creatures_list:
            creature_movement(cur_creature)

        #After moving every creature, check if they can eat and handle if they can
        for cur_creature in cur_creatures_list:
            cur_food_index = 0
            #Check if the creatures have eaten a food, and update the food list if they have. While loop instead of a
            #for loop because it makes handling simpler.
            while cur_food_index < len(food_list):
                cur_food = food_list[cur_food_index]
                if creature_eat_handler(cur_creature, cur_food):
                    #Update the food list and decrement the index counter by 1 to account for the increment by 1 soon
                    del food_list[cur_food_index]
                    cur_food_index -= 1