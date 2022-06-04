class DLinkedList:
    """A custom data structure for keeping track of things more efficiently than using normal arrays. Each node must
    be a DNode object in order to work properly.

    Parameters
    ------------
    head_val: The first node in the Doubly Linked List"""

    def __init__(self, head_val=None):
        self.head_val = head_val

    def add_in_front(self, new_node):
        new_node.node_clip()
        old_head = self.head_val
        if old_head is None:
            self.head_val = new_node
            return

        old_head.back = new_node
        new_node.front = old_head
        self.head_val = new_node

    def remove_head(self):
        old_head = self.head_val
        if old_head is None:
            print("ERROR: DLINKEDLIST IS EMPTY")
            return

        new_head = old_head.front
        new_head.back = None
        self.head_val = new_head
        old_head.node_clip()
        return old_head

    def add_at_end(self, new_node):
        new_node.node_clip()
        this_node = self.head_val
        if this_node is None:
            self.head_val = new_node
            return

        while this_node.front is not None:
            this_node = this_node.front

        this_node.front = new_node
        new_node.back = this_node

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
        new_node.node_clip()
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

    def delete_all_nodes(self):
        cur_head = self.head_val
        if cur_head is None:
            return

        while cur_head is not None:
            temp_node = cur_head.front
            del cur_head.data
            del cur_head
            cur_head = temp_node

        del cur_head
        del self.head_val
        self.head_val = None

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

        target_node.node_clip()
        return target_node

    def replace_node(self, target_node, replacement_node):
        find_node = self.head_val
        while find_node is not target_node:
            if find_node.front is None:
                print("ERROR: DID NOT FIND TARGET NODE")
                return

            find_node = find_node.front

        replacement_node.node_clip()
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

        target_node.node_clip()
        return target_node

    def find_length(self):
        cur_node = self.head_val
        this_len = 0
        while cur_node is not None:
            cur_node = cur_node.front
            this_len += 1

        return this_len

    def find_node_by_data(self, target_data):
        """This method will input the target data you want to locate and output the node containing that data and the
        node's index."""
        if target_data is None:
            print("ERROR: target_data MUST NOT BE NONE")
            return -2, -2

        return_node = self.head_val
        node_index = 0
        while return_node is not None:
            if return_node.data is target_data:
                return return_node, node_index

            return_node = return_node.front
            node_index += 1

        #Indicating that the target_data was not found
        return -1, -1

    def find_node_by_index(self, node_index):
        if node_index < 0:
            print("ERROR: node_index MUST BE AT LEAST 0")
            return

        cur_node = self.head_val
        for times in range(node_index):
            cur_node = cur_node.front

        return cur_node


def make_empty_dll(length, data_type=None):
    new_dll = DLinkedList()
    for times in range(length):
        new_dll.add_in_front(DNode(data_type))

    return new_dll

class DNode:
    """The object that will work with the LinkedList to store data and 2 pointers, a front and a back

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
        del self.data
        self.data = None
        self.front = None
        self.back = None

    def node_clip(self):
        self.front = None
        self.back = None
