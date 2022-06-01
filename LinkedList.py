class DLinkedList:
    """A custom data structure for keeping track of things more efficiently than using normal arrays. Each node must
    be a DNode object in order to work properly.

    Parameters
    ------------
    head_val: The first node in the Doubly Linked List"""

    def __init__(self, head_val=None):
        self.head_val = head_val

    def add_in_front(self, new_node):
        old_node = self.head_val
        old_node.back = new_node
        new_node.front = old_node
        self.head_val = new_node

    def remove_head(self):
        old_head = self.head_val
        if old_head is None:
            print("ERROR: DLINKEDLIST IS EMPTY")
            return

        new_head = old_head.front
        new_head.back = None
        self.head_val = new_head
        old_head.node_strip()
        return old_head

    def add_at_end(self, new_node):
        this_node = self.head_val
        while this_node.front is not None:
            this_node = this_node.front

        this_node.front = new_node

    def remove_tail(self):
        this_node = self.head_val
        if this_node is None:
            print("ERROR: DLINKEDLIST IS EMPTY")
            return

        while this_node.front is not None:
            this_node = this_node.front

        new_tail = this_node.back
        new_tail.front = None
        this_node.strip_node()
        return this_node

    def add_in_between(self, previous_node, new_node):
        find_node = self.head_val
        while find_node.front is not None:
            if find_node is previous_node:
                break

            find_node = find_node.front

        if find_node is not previous_node:
            print("ERROR: DID NOT FIND PREVIOUS NODE")
            return

        if find_node.front is None:
            find_node.front = new_node
            return

        if find_node.back is None:
            new_node.front = find_node
            find_node.back = new_node
            self.head_val = new_node
            return

        find_node_after = find_node.front
        find_node.front = new_node
        new_node.back = find_node
        new_node.front = find_node_after
        find_node_after.back = new_node

    def remove_node(self, target_node):
        find_node = self.head_val
        while find_node is not target_node:
            if find_node.front is None:
                print("ERROR: DID NOT FIND TARGET NODE")
                return

            find_node = find_node.front

        if find_node.back is None and find_node.front is not None:
            new_head = find_node.front
            new_head.back = None
            self.head_val = new_head

        elif find_node.back is not None and find_node.front is None:
            new_tail = find_node.back
            new_tail.front = None

        elif find_node.back is not None and find_node.front is not None:
            find_node_back = find_node.back
            find_node_front = find_node.front
            find_node_back.front = find_node_front
            find_node_front.back = find_node_back

        elif find_node.back is None and find_node.front is None:
            self.head_val = None

        target_node.node_strip()
        return target_node

    def replace_node(self, target_node, replacement_node):
        find_node = self.head_val
        while find_node is not target_node:
            if find_node.front is None:
                print("ERROR: DID NOT FIND TARGET NODE")
                return

            find_node = find_node.front

        replacement_node.node_strip()
        if find_node.back is None and find_node.front is not None:
            new_head = replacement_node
            new_head.back = None
            new_head.front = find_node.front
            self.head_val = new_head

        elif find_node.back is not None and find_node.front is None:
            new_tail = replacement_node
            new_tail_back = find_node.back
            new_tail.front = None
            new_tail.back = new_tail_back
            new_tail_back.front = new_tail

        elif find_node.back is not None and find_node.front is not None:
            find_node_back = find_node.back
            find_node_front = find_node.front
            find_node_back.front = replacement_node
            replacement_node.back = find_node_back
            replacement_node.front = find_node_front
            find_node_front.back = replacement_node

        elif find_node.back is None and find_node.front is None:
            self.head_val = replacement_node

        target_node.node_strip()
        return target_node


class DNode:
    """The object that will work with the LinkedList to store data and 2 pointers, a front and back

    Parameters
    ------------
    data: The object that this Node is storing
    front: A pointer to the next node in front of this one
    back: A pointer to the previous node behind this one"""

    def __init__(self, data=None, front=None, back=None):
        self.data = data
        self.front = front
        self.back = back

    def node_strip(self):
        self.front = None
        self.back = None
