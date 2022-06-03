import copy
import random as rand
import math as m
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.pyplot import plot

import Map
import Creature
import Food
import LinkedList

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

#Initializing this variable before the loop, so it doesn't reset every time the loop starts over
"""
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
"""
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

