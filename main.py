import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('tkagg')

import Map
import Creature

t_pi = 2 * m.pi

#Map Instance Parameters
map_radius = 10.0
food_radius = 9.0
time_step = 0.01
initial_creatures_count = 1
initial_food_amount = 1
total_days = 1

the_map = Map.Map(map_radius, food_radius, time_step, initial_creatures_count, initial_food_amount, total_days)

#Creature Static Parameters
eat_radius = 0.15
max_j_theta = 55.0
max_offset_percent = 0.15
base_energy = 30.0

Creature.Creature.eat_radius = eat_radius
Creature.Creature.max_j_theta = max_j_theta
Creature.Creature.max_offset_percent = max_offset_percent
Creature.Creature.base_energy = base_energy

########################################################################################################################
########################################################################################################################
#Simulation Loop
########################################################################################################################

#Debugging stuff
my_x_vals = []
my_y_vals = []

#Initializing things before the loop begins
the_map.initialize_creature_lists()
creature_list_list = the_map.creature_children

#Do this everyday
for cur_day_index in range(total_days):
    print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n", "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n",
          "DAY " + str(cur_day_index+1), "\n=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n",
          "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+")
    the_map.food_list_reset()
    food_list_today = the_map.food_children

    cur_creatures_list = (creature_list_list.find_node_by_index(cur_day_index)).data

    #While creatures can move, keep looping
    initial_creatures_moving = cur_creatures_list.find_length()
    tired_creatures = 0
    food_on_map = food_list_today.find_length()

    # While there are still creatures moving and food on the map => Move a creature => Check if any food is within its
    # vicinity after moving
    while (initial_creatures_moving - tired_creatures) * food_on_map > 0:
        tired_creatures = 0
        cur_creature_node = cur_creatures_list.head_val

        # For Debugging ONLY
        this_x, this_y = Map.polar_to_cartesian(cur_creature_node.data.radius, cur_creature_node.data.theta)
        my_x_vals.append(this_x)
        my_y_vals.append(this_y)
        # For Debugging ONLY

        while cur_creature_node is not None:
            cur_food_node = food_list_today.head_val
            cur_creature = cur_creature_node.data
            has_moved = cur_creature.creature_movement()
            tired_creatures += 0 if has_moved else 1

            # For Debugging ONLY
            this_x, this_y = Map.polar_to_cartesian(cur_creature_node.data.radius, cur_creature_node.data.theta)
            my_x_vals.append(this_x)
            my_y_vals.append(this_y)
            # For Debugging ONLY

            while (cur_food_node is not None) and has_moved:
                next_food_node = cur_food_node.front
                was_eaten = the_map.eat_food_handler(cur_creature_node, cur_food_node)
                food_on_map -= 1 if was_eaten else 0
                cur_food_node = next_food_node

            cur_creature_node = cur_creature_node.front

    # After all creatures have moved and/or there is no more food on the map, decide whether each creature should move
    # to the next generation, reproduce or die
    cur_creature_node = cur_creatures_list.head_val
    while cur_creature_node is not None:
        cur_creature = cur_creature_node.data
        the_map.creature_next_generation_handler(cur_creature_node, cur_day_index)
        cur_creature_node = cur_creature_node.front
    #CONTINUE WRITING SIMULATION CODE

print("done")

########################################################################################################################
########################################################################################################################
#Data Processing
########################################################################################################################
plt.plot(my_x_vals, my_x_vals)
plt.show()
