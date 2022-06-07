import math as m
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('tkagg')

import Map
import Creature

t_pi = 2 * m.pi

########################################################################################################################
########################################################################################################################
#User Variables
########################################################################################################################

#Map Instance Parameters
map_radius = 8.0
food_radius = 7.5
time_step = 0.01
initial_creatures_count = 6
initial_food_amount = 90
total_days = 8

#Creature Static Parameters
eat_radius = 0.1
max_v_theta = 0.66
max_a_theta = 0.1
max_j_theta = 2.2
max_offset_percent = 0.15
base_energy = 30.0

########################################################################################################################
########################################################################################################################
#Object Initialization
########################################################################################################################

the_map = Map.Map(map_radius, food_radius, time_step, initial_creatures_count, initial_food_amount, total_days)

Creature.Creature.eat_radius = eat_radius
Creature.Creature.max_v_theta = max_v_theta
Creature.Creature.max_a_theta = max_a_theta
Creature.Creature.max_j_theta = max_j_theta
Creature.Creature.max_offset_percent = max_offset_percent
Creature.Creature.base_energy = base_energy

########################################################################################################################
########################################################################################################################
#Simulation Loop
########################################################################################################################

##Debugging stuff
#my_x_vals = []
#my_y_vals = []
##Debugging stuff

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

        ## For Debugging ONLY
        #this_x, this_y = Map.polar_to_cartesian(cur_creature_node.data.radius, cur_creature_node.data.theta)
        #my_x_vals.append(this_x)
        #my_y_vals.append(this_y)
        ## For Debugging ONLY

        while cur_creature_node is not None:
            cur_food_node = food_list_today.head_val
            cur_creature = cur_creature_node.data
            has_moved = cur_creature.creature_movement()
            tired_creatures += 0 if has_moved else 1

            ## For Debugging ONLY
            #this_x, this_y = Map.polar_to_cartesian(cur_creature_node.data.radius, cur_creature_node.data.theta)
            #my_x_vals.append(this_x)
            #my_y_vals.append(this_y)
            ## For Debugging ONLY

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

day_arr = []
live_creatures_arr = []
dead_creatures_arr = []
survivor_creatures_arr = []
fecund_creatures_arr = []
for cur_day_index in range(total_days):
    day_arr.append(cur_day_index+1)
    live_creatures_arr.append(the_map.creature_children.find_node_by_index(cur_day_index).data.find_length())
    dead_creatures_arr.append(the_map.dead_creatures_data.find_node_by_index(cur_day_index).data.find_length())
    survivor_creatures_arr.append(the_map.survivor_creatures_data.find_node_by_index(cur_day_index).data.find_length())
    fecund_creatures_arr.append(the_map.fecund_creatures_data.find_node_by_index(cur_day_index).data.find_length())

ind = np.arange(total_days)

fig, ax = plt.subplots()
rects_1 = ax.bar(ind + 0.00, live_creatures_arr, color='black', width=0.2)
rects_2 = ax.bar(ind + 0.20, dead_creatures_arr, color='r', width=0.2)
rects_3 = ax.bar(ind + 0.40, survivor_creatures_arr, color='b', width=0.2)
rects_4 = ax.bar(ind + 0.60, fecund_creatures_arr, color='g', width=0.2)

ax.set_ylabel('Number of Creatures')
ax.set_title('Creatures Data')
ax.set_xticks(ind)

ax.legend((rects_1[0], rects_2[0], rects_3[0], rects_4[0]), ('Living', 'Dead', 'Survivors', 'Fecund'))

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')


autolabel(rects_1)
autolabel(rects_2)
autolabel(rects_3)
autolabel(rects_4)

plt.show()


#Debugging stuff
#circle2 = plt.Circle((0, 0), map_radius, color='r', fill=False)
#plt.gca().add_patch(circle2)
#plt.scatter(my_x_vals, my_y_vals, s=0.01)
#plt.show()
#print("done 2")
##Debugging stuff