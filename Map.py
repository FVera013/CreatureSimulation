import Creature
import Food
import LinkedList

import math as m
import random as rand

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
        ***creature_children: A child class (must be a 2D instance of DLinkedList containing creature objects in order
        to work properly)
        \b
        food_children: A child class (must be an instance of DLinkedList containing food objects in order to
        work properly)
        \b
        ***dead_creatures_data: A data storage class for creatures that died (must be a 2D instance of DLinkedList
        containing creature objects in order to work properly)
        \b
        ***fecund_creatures_data: A data storage class for creatures that reproduced (must be a 2D instance of
        DLinkedList containing creature objects in order to work properly)
        \b
        ***survivor_creatures_data: A data storage class for creatures that survived (must be a 2D instance of
        DLinkedList containing creature objects in order to work properly)"""

    def __int__(self, map_radius, food_radius, time_step, initial_creatures_count, initial_food_amount, total_days):
        self.map_radius = map_radius
        self.food_radius = food_radius
        self.time_step = time_step
        self.initial_creatures_count = initial_creatures_count
        self.initial_food_amount = initial_food_amount
        self.total_days = total_days
        self.creature_children = LinkedList.make_empty_dll(total_days, LinkedList.DLinkedList)
        self.food_children = LinkedList.DLinkedList()
        self.dead_creatures_data = LinkedList.make_empty_dll(total_days, LinkedList.DLinkedList)
        self.fecund_creatures_data = LinkedList.make_empty_dll(total_days, LinkedList.DLinkedList)
        self.survivor_creatures_data = LinkedList.make_empty_dll(total_days, LinkedList.DLinkedList)

    def initialize_creature_list(self):
        first_day_creature_list = self.creature_children.head_val
        for times in range(self.initial_creatures_count):
            cur_creature = Creature.Creature().creature_reset()
            cur_creature_node = LinkedList.DNode(cur_creature)
            first_day_creature_list.add_in_front(cur_creature_node)

    def food_list_reset(self):
        food_list = self.food_children
        if food_list.head_val is not None:
            food_list.delete_all_nodes()

        for times in range(self.initial_food_amount):
            cur_radius = self.food_radius * rand.random()
            eat_radius = Creature.Creature.eat_radius
            cur_food = Food(cur_radius, (t_pi * rand.random()) % t_pi, m.atan(eat_radius / cur_radius))
            cur_food_node = LinkedList.DNode(cur_food)
            food_list.add_in_front(cur_food_node)

    def eat_food_handler(self, this_creature_node, this_food_node):
        this_creature = this_creature_node.data
        this_food = this_food_node.data
        if this_creature.creature_eat_handler(this_food):
            # old_food_node and this_food_node should be the exact same, but renaming this variable so using the
            # renamed version should not be an issue, I just think it's better consistency (F)
            old_food_node = self.food_children.remove_node(this_food_node)
            old_food_node.node_strip()
            del old_food_node

    def creature_next_generation_handler(self, creature_node, cur_day_index):
        this_creature = creature_node.data
        this_food_eaten = this_creature.food_eaten
        next_day_creature_dll = None
        if cur_day_index + 1 < self.total_days:
            next_day_creature_dll = self.creature_children.find_node_by_index(cur_day_index + 1)

        if this_food_eaten == 0:
            this_dead_list = self.dead_creatures_data.find_node_by_index(cur_day_index)
            this_dead_list.add_in_front(creature_node.copy())

        if this_food_eaten == 1:
            this_survivor_list = self.survivor_creatures_data.find_node_by_index(cur_day_index)
            this_survivor_list.add_in_front(creature_node.copy())
            if next_day_creature_dll is not None:
                next_day_creature_dll.add_in_front(creature_node.copy())

        elif this_food_eaten > 1:
            this_fecund_list = self.fecund_creatures_data.find_node_by_index(cur_day_index)
            this_fecund_list.add_in_front(creature_node.copy())
            if next_day_creature_dll is not None:
                next_day_creature_dll.add_in_front(creature_node.copy())
                next_day_creature_dll.add_in_front(creature_node.copy())


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
