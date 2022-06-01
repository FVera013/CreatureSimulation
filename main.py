import copy
import random as rand
import math as m
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.pyplot import plot

import Creature

t_pi = 2 * m.pi

initial_creatures_count = 10
initial_food_amount = 500
total_days = 30
eat_radius = 0.1

#defines the max jerk_theta, third derivative of theta, the creature can achieve
max_j_theta = 1

#max percent
max_offset_percent = 0.01
map_radius = 18.0
food_radius = 8.0
time_step = 1
total_time_steps_per_day = time_step

class Food:
    """The Food object that creatures can consume

    Parameters
    ------------
    radius: the polar coordinate r of the Food object
    theta: the polar coordinate theta of the Food object
    theta_lim: how close a Creature needs to be to this Food in order for it to possibly be withing eating range"""
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
        if theta!=-1: theta = ((quadrant-1) * (m.pi/2)) + m.atan( abs( (cart_y/cart_x) ** ((-1)**(quadrant-1)) ) )
        theta = theta % t_pi

    return r, theta

def position_checker(this_creature):
    if this_creature.radius > map_radius:
        setattr(this_creature, 'energy_left', 0)

def creature_movement(this_creature):
    """A function that returns an array. The array determines the creature's new parameters after moving. If the
    creature did not move, an empty array will be returned."""
    print("In creature_movement function")
    cur_energy = this_creature.energy_left

    if cur_energy <= 0:
        return []

    #Third derivative of orientation is random every time step
    this_j_theta = (rand.random()*2 - 1) * max_j_theta

    cur_radius = this_creature.radius
    cur_theta = this_creature.theta

    start_x, start_y = polar_to_cartesian(cur_radius, cur_theta)

    cur_speed = this_creature.speed
    #Current orientation, first derivative of orientation, and second derivative of orientation, respectively.
    cur_o_theta = this_creature.direction
    cur_v_theta = this_creature.d1_theta
    cur_a_theta = this_creature.d2_theta

    cur_a_theta += (time_step*this_j_theta) % t_pi
    cur_v_theta += (time_step*cur_a_theta + (1/2)*(time_step**2)*this_j_theta) % t_pi
    cur_o_theta += (time_step*cur_v_theta + (1/2)*(time_step**2)*cur_a_theta + (1/6)*(time_step**3)*this_j_theta) % t_pi

    d_x, d_y = polar_to_cartesian(cur_speed*time_step, cur_o_theta)
    end_r, end_theta = cartesian_to_polar(start_x + d_x, start_y + d_y)

    cur_energy -= time_step * (cur_speed ** 2)
    if end_r >= map_radius or cur_energy <= 0:
        cur_energy = 0

    return [end_r, end_theta, cur_o_theta, cur_v_theta, cur_a_theta, cur_energy]

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
    past_list_index = (cur_list_index + 1) % 2

    creature_pops_list[past_list_index].append(this_creature)

    if this_food_eaten == 0:
        Creature.creature_reset(this_creature)
        dead_creatures_list[cur_day_index].append(this_creature)
    elif this_food_eaten == 1:
        Creature.creature_reset(this_creature)
        living_creatures_list[cur_list_index].append(this_creature)
    elif this_food_eaten > 1:
        Creature.creature_reset(this_creature)
        child_creature = copy.deepcopy(this_creature)
        living_creatures_list[cur_list_index].append(this_creature)
        living_creatures_list[cur_list_index].append(child_creature)

def food_list_reset():
    food_list.clear()
    for i in range(initial_food_amount):
        cur_radius = food_radius * rand.random()
        food_list.append(Food(cur_radius, (t_pi * rand.random()) % t_pi, m.atan(eat_radius / cur_radius)))

living_creatures_list = [[], []]
final_creatures_list = []

for each in range(initial_creatures_count):
    cur_theta = (t_pi * rand.random()) % t_pi
    cur_offset_percent = (1 + max_offset_percent * (2 * rand.random() - 1))
    cur_direction = ((cur_theta + m.pi) * cur_offset_percent) % t_pi
    living_creatures_list[0].append(Creature(map_radius*0.98, cur_theta, cur_direction))

creature_pops_list = []
dead_creatures_list = []
for day in range(total_days):
    creature_pops_list.append([])
    dead_creatures_list.append([])

food_list = []

########################################################################################################################
########################################################################################################################
#Simulation Loop
########################################################################################################################

#Initializing this variable before the loop so it doesn't reset every time the loop starts over
creature_list_index = 0

#Need to repeat this for every day
for day in range(total_days):
    #Reset food_list at the very beginning of every day
    food_list_reset()

    #Update creature_list_index everytime the loop restarts
    creature_list_index = day % 2

    #The rest of the logic for the simulation
    cur_creatures_list = living_creatures_list[creature_list_index]
    creatures_moving = len(cur_creatures_list)

    #While loop instead of a for loop, because it makes handling simpler
    while creatures_moving > 0:
        #Move each creature in order
        for cur_creature in cur_creatures_list:
            new_creature_params = []
            new_creature_params.clear()
            new_creature_params = creature_movement(cur_creature)
            #What to do if the list returned empty (creature had no energy at function call)
            if len(new_creature_params) == 0:
                creature_next_generation_handler(cur_creature, creature_list_index, day)
                continue

            #What to do if the list returned with 0 current energy
            if new_creature_params[5] <= 0:
                creature_next_generation_handler(cur_creature, creature_list_index, day)
                continue

            #What to do if the list returned with more than 0 current energy

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

                #Increment index counter
                cur_food_index += 1

        #Check if there's still food on the map
        if len(food_list) == 0:
            creatures_moving = 0

    #Moving the next generation of creatures to the next cur_creatures list and recording data
    next_creature_list_index = (creature_list_index + 1) % 2
    #Updating the current list that was being worked with, the one that will be worked with and other data storage lists
    for creature in cur_creatures_list:
        creature_next_generation_handler(creature, creature_list_index, day)

creature_pops_list[total_days-1].append(copy.deepcopy(living_creatures_list[creature_list_index]))

########################################################################################################################
########################################################################################################################
#Data Processing
########################################################################################################################

#Plotting the Data
x_axes = []
y_axes = []

#Intermediate lists
x_temp = []
y_temp = []

#Adding the data for dead creatures per day
for i in range(total_days):
    x_temp.append(i+1)
    y_temp.append(len(dead_creatures_list[i]))

x_axes.append(x_temp.copy())
y_axes.append(y_temp.copy())

x_temp.clear()
y_temp.clear()

#Adding the data for population per day
for i in range(total_days):
    x_temp.append(i+1)
    y_temp.append(len(creature_pops_list[i]))

x_axes.append(x_temp.copy())
y_axes.append(y_temp.copy())

plot(x_temp, y_temp)

x_temp.clear()
y_temp.clear()

