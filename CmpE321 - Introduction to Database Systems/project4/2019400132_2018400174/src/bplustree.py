"""
What is order?
If order = M, then following conditions must be satisfied:
1) Maximum number of keys in a node can be M - 1
2) Maximum number of children per node can be M


Some B+ Tree features:
1) A non-leaf node with k children has k - 1 keys
"""


"""
Binary search algorithm
It returns:

1) Index of the key if it's present in lst
2) Index of the element which is the biggest element is the lst that is smaller than lst (-1 if none)

How to use it:
When the data is returned, check if lst[mid] == key. If so, then you found the element you are looking for.
If not, then branch into node.children[mid+1].
"""

import math


def binary_search(lst, key):
    if(not lst): return (-1, False)

    lo = 0
    hi = len(lst) - 1

    while(lo < hi):
        mid = lo + (hi - lo)//2
        if(lst[mid] < key): lo = mid + 1
        elif(lst[mid] > key): hi = mid - 1
        else: return (mid, True)  #found
    
    mid = lo + (hi - lo) // 2
    
    if(mid < 0): 
        return (-1, False)  # not found
    else: 
        mid = mid - 1 if (lst[mid] > key) else mid 
        if(lst[mid] == key): return (mid, True)  # found
        else: return (mid, False)  # not found
    
class Node:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.values = []       # either holds data or children nodes
        self.nextNode = None    # next key
        self.previousNode = None
        self.parent = None
        self.isLeaf = True
        self.page_index = None
    
    def add(self, key, value):
        """Add a key-value pair to the node."""
        if not self.keys: # empty
            self.keys.append(key)
            self.values.append([value])
            return True

        # else
        (idx, isPresent) = binary_search(self.keys, key)

        if(isPresent):
            # if new key matches existing key, add to the list of the values
            return False
        elif(idx != len(self.keys) - 1 and idx != -1):
            # key is not present, and it should be located somewhere in between
            self.keys = self.keys[:idx+1] + [key] + self.keys[idx+1:]
            self.values = self.values[:idx+1] + [[value]] + self.values[idx+1:]
        elif(idx == len(self.keys) - 1):
            # key is not present and it's greater than all other elements
            self.keys.append(key)
            self.values.append([value])
        else:  # (idx == -1)
            self.keys.insert(0, key)
            self.values.insert(0, [value])
        return True

    def split(self):
        prev = self.previousNode
        nex = self.nextNode

        "Split the node into two and store them as child nodes"
        left = Node(self.order)
        right = Node(self.order)
        mid = self.order // 2 # if M = 4 --> mid = 2 (left biased)
                                    # if M = 3 --> mid = 1 
        

        if(self.isLeaf):                      
            # we are going to split a leaf node.
            """
            self.keys = [10, 20, 30, 40]
            self.values = [[5], [15], [25], [35]]

            expected:
            left.keys = [10, 20]
            left.values = [[5], [15]]

            right.keys = [30, 40]
            right.values = [[25], [35]]

            mid = 2
            self.keys[2:] = [30, 40]
            self.values[2:] = [25, 35]
            """
            right.keys = self.keys[mid:]
            right.values = self.values[mid:]

            left.keys = self.keys[:mid]  # mid is not included
            left.values = self.values[:mid]
        else:
            """
            self.keys = [10, 20, 30, 40]
            self.values = [node1, node2, node3, node4, node5]

            expected:
            parent.keys = [30]
            parent.values = [left, right]

            left.keys = [10, 20]
            left.values = [node1, node2, node3]

            right.keys = [40]
            right.values = [node4, node5]

            mid = 2
            self.keys[2 + 1:] = [40]
            self.values[2 + 1:] = [node4, node5]

            self.keys[:2] = [10, 20]
            self.values[:3] = [node1, node2, node3] 
            """
            right.keys = self.keys[mid+1:]
            right.values  = self.values[mid+1:]

            left.keys = self.keys[:mid]  # mid is not included
            left.values = self.values[:mid+1]
        # when the node is split, set the parent key to the left-most key of the right child node

        self.keys = [self.keys[mid]]
        # this part is important. This node is no longer a leaf node,
        # therefore it cannot contain actual values. What it can contain instead
        # is pointer to children nodes. self.values now contain left and right children.
        self.values = [left, right] 
        self.isLeaf = False  # it's no longer a leaf
        
        left.isLeaf = not(isinstance(left.values[0], Node)) # check if left is leaf node
        right.isLeaf = left.isLeaf

        if(not left.isLeaf):
            for child in left.values:
                child.parent = left
            for child in right.values:
                child.parent = right

        left.nextNode = right # pointers between leaf nodes
        right.previousNode = left

        left.previousNode = prev
        if(prev is not None): prev.nextNode = left
        
        right.nextNode = nex
        if(nex is not None): nex.previousNode = right

        # At this point we can delete the nextNode pointer of child since it's not leaf anymore.
        # But I won't delete it for now, maybe it'll become handy to keep them at some point.
        

        return (left, self, right)

    def is_full(self):
        "split is required if full"
        return (len(self.keys) > self.order - 1) # maximum M - 1 keys

    def __repr__(self):
        return "Node object with keys :" + ", ".join([str(x) for x in self.keys])


class BPlusTree:
    def __init__(self, order):
        self.root = Node(order) # create a root
        self.root.page_index = 0
        self.order = order


    @staticmethod
    def _find(node, key):
        """
        Return the index where the key should be inserted
        and the list of values at that index.

        for example:
            keys = [10, 20, 30]
            values = [[1,2],[15,16],[25,26]]
            query key = 5
            return = (0, [1, 2], False)
        """
        (idx, isPresent) = binary_search(node.keys, key)
        if(isPresent): # already present
            return (idx, node.values[idx], True)  # True indicates that it's already present
        else:
            vals = [] if (len(node.values) <= idx + 1) else node.values[idx + 1]
            return (idx + 1, vals, False)


    def search(self, key):
        """Returns a value for a given key, and None if the key does not exist."""
        node = self.root

        """
        Be careful!
        Let's say you are not at a leaf node and looking for 20.
        node.keys = [20, 30]
        node.values = [node1, node2, node3]
        We have to branch into node2. However _find returns node1 since it returns the 
        "the index where the key should be inserted and the list of values at that index".

        Check that condition explicitly. 
        """
        while (not node.isLeaf):
            (index, child, onSpot) = self._find(node, key)

            if(onSpot): node = node.values[index + 1]
            else: node = child
            

        # now, we are at a leaf node (hopefully containing our key)

        (idx, isPresent) = binary_search(node.keys, key)
        if(isPresent): return node.page_index
        else: return None    # not found


    @staticmethod
    def _merge(parent, child):
        """
        Merge child into a proper place in the parent.
        Due to the splitting mechanism, child is in the following form:
        child.keys = [x]  # one key
        child.values = [left, right]

        we have to find a proper place for that key in the parent
        """
        key = child.keys[0]
        (idx, values, onSpot) = BPlusTree._find(parent, key)
        # what happens if key is already present in the tree = I don't know

        
        """
        what did _find return?
            for example:
        parent keys = [10, 20, 30]
        parent values = [node1, node2, node3, node4]
        child key = 25
        return = (2, [5, 6], False)

        we have to insert the child key at the index 2.
        new parent should be something like this:
        parent keys = [10, 20, 25, 30]
                              idx = 2
        parent values = [node1, node2, left, right, node4]
                                       idx = 2
        """

        if(idx < len(parent.keys)):
            # we have to insert it into index idx
            parent.keys = parent.keys[:idx] + [child.keys[0]] + parent.keys[idx:]
            parent.values = parent.values[:idx] + child.values + parent.values[idx+1:]
        else: # append
            parent.keys.append(child.keys[0])
            parent.values[-1] = child.values[0]   # replace child with left
            parent.values.append(child.values[1]) # add right

            # now, we have a link from parent to left and right children. garbage collection will take care of the node 'child'

    # Pseudocode in the book contains entry rather than key. Each entry has a unique key.
    # We can convert our implementation to that very easily. For now, I'm keeping insertion function with key rather than entry.
    def insert(self, key, value, fileHandler):
        """
        Insert a key-value pair after arriving at a leaf node.
        If the leaf node becomes full, split it into two.
        """

        child = self.root
        while(not child.isLeaf):
            (index, node, onSpot) = self._find(child, key)

            if(onSpot): child = child.values[index + 1]
            else: child = node
        
        # If key is already present, then add the new value (do not delete the previous values)
        success = child.add(key, 0)
        if success:
            fileHandler.write_record(child.page_index, value)

            # now we have to check if there is a split situation.
            while(child.is_full()):
                child_was_leaf = child.isLeaf
                (left, child, right) = child.split()
                if child_was_leaf:
                    left.page_index = child.page_index
                    right.page_index = fileHandler.get_next_available_page_index()
                    child.page_index = None

                    fileHandler.split_page(left.page_index, right.keys[0])
                
                # now we have to take the child and insert it to a proper place among parent's keys and values
                # but before doing that, check if parent is None (it means that we are at root)
                parent = child.parent

                if(parent is None):
                    # This means that child was our root.
                    # Let's keep it that way (it's modified due to the splitting of course)
                    left.parent = child   # set parents
                    right.parent = child  # set parents
                else:
                    self._merge(parent, child)

                    left.parent = parent
                    right.parent = parent
                    child = parent # now let's do the same thing for parent
        return success

        
    def _min(self, node):  # find minimum key in the subtree with root = node
        while(not node.isLeaf):
            node = node.values[0]
        
        return node.keys[0]


    """
    Before deletion, let's remember the rule
    1) A node can have a maximum of M children
    2) A node can contain a maximum of M - 1 keys
    3) A node should have a minimum of ceil(M/2) children
    4) A node (except the root) should contain a minimum of ceil(M/2) - 1 keys.

    We check explicitly 1 and 2. 3 and 4 are satisfied automatically because of our insertion
    mechanism. However, in deletion we have to check them explicitly.
    """
    def delete(self, key, fileHandler):
        x, status = self._delete(self.root, key, None, 0, fileHandler)
        if(self.root.values and not self.root.keys):  # self.root still exists but it has no key
            self.root = self.root.values[0]
        self.root.parent = None
        return status

    def replace_key_with_min(self, node, key):
        (idx, isPresent) = binary_search(node.keys, key)
        if(isPresent):
            node.keys[idx] = self._min(node.values[idx + 1])

    # parent.values[index] = node
    def _delete(self, node, key, idx_of_removed_child, index, fileHandler):
        if(not node.isLeaf):  
            (nextIndex, child, onSpot) = self._find(node, key)
            if(onSpot): 
                child = node.values[nextIndex + 1]
                nextIndex += 1
            
            """
            If onSpot, meaning that if key has an exact match in the keys of the node
            we have to increment the index by one because what we are looking for is stored
            in node.values[index + 1], not in node.values[index].
            """
 
            # we found the correct subtree to continue with.
            idx_of_removed_child, status = self._delete(child, key, idx_of_removed_child, nextIndex, fileHandler) # recursive delete
            # leaf node is deleted
            if(idx_of_removed_child is None): 
                self.replace_key_with_min(node, key)
                return None, status
            else:
                # remove old_child_entry from 
                del node.values[idx_of_removed_child]  # delete subtree
                del node.keys[idx_of_removed_child - 1]

                # after this point, we don't have to think about child nodes. Our work is done, now it's time to check this level.
     
                min_keys = math.ceil(self.order / 2) - 1
                if(len(node.keys) >= min_keys or node is self.root):
                    self.replace_key_with_min(node, key)
                    return None, status
                else: # again it doesn't satisfy minimum constraint
                    siblings = node.parent.values

                    # siblings[index] = node
                    S = None
                    left = False
                    # first check left
                    if(index > 0 and len(siblings[index - 1].keys) >= min_keys + 1): # left
                        S = siblings[index - 1]
                        left = True
                    elif (index + 1< len(siblings) and len(siblings[index + 1].keys) >= min_keys + 1):  # right
                        S = siblings[index + 1]
                        left = False
                    if(S is not None): # S is either left or right sibling and it has extra entries
                        if(left): # S is at left
        
                            lastKey = S.keys.pop()
                            lastChild = S.values.pop()

                            node.keys.insert(0, node.parent.keys[index - 1])
                            node.values.insert(0, lastChild)
                            node.parent.keys[index - 1] = lastKey

                            lastChild.parent = node

                        else:  # S is at the right
                            firstKey = S.keys.pop(0)
                            firstChild = S.values.pop(0)

                            node.values.append(firstChild)
                            node.keys.append(node.parent.keys[index] )
                            node.parent.keys[index] = firstKey  # for max degree = 3, min key = 1. We know that len(S.keys) > min + 1  

                            firstChild.parent = node

                        idx_of_removed_child = None

                    else:  # merge node and S
                        if(index > 0): 
                            S = siblings[index - 1] # left
                            left = True
                        else: 
                            S = siblings[index + 1]          # right
                            left = False
                        
                        
                        if(left):   # S is on left, node is on right
                            idx_of_removed_child = index  # remove the right node
                            S.keys.append(node.parent.keys[index - 1])
                            S.keys += node.keys # take all keys of node to S
                            S.values += node.values
                            S.nextNode = node.nextNode  # node is removed

                            for child in node.values:
                                child.parent = S
                                
                            if(node.nextNode is not None): node.nextNode.previousNode = S
                            self.replace_key_with_min(S, key)

                        else:  # S is on right, node is on left
                            
                            idx_of_removed_child = index + 1 # remove the right node (S)
                            node.keys.append(node.parent.keys[index])
                            node.keys += S.keys
                            node.values += S.values
                            node.nextNode = S.nextNode

                            for child in S.values:
                                child.parent = node
                            
                            if(S.nextNode is not None): S.nextNode.previousNode = node
                            self.replace_key_with_min(node, key)
            
            # replace the key in the intermediate node if necessary
            self.replace_key_with_min(node, key)
            
            return idx_of_removed_child, status
        else:
            
            (idx, isPresent) = binary_search(node.keys, key)
            if(not isPresent): return None, False  # not found
            fileHandler.delete_record(node.page_index, node.keys[idx])
        
            min_keys = math.ceil(self.order / 2) - 1
            
            if(len(node.keys) >= min_keys + 1 or node is self.root):  # if node is root, then continue regardless of the condition
                del node.keys[idx] 
                del node.values[idx]
                return None, True
            else:   
                # not enough keys in the leaf node
                # we have to find a sibling
                # siblings are the nodes with the same parent of this node
                # we can't use nextNode because it may not be a sibling.
    
                siblings = node.parent.values
                
                # siblings[index] = node
                S = None
                left = False
                # first check left
                if(index > 0 and len(siblings[index - 1].keys) >= min_keys + 1): # left
                    S = siblings[index - 1]
                    left = True
                elif (index + 1 < len(siblings) and len(siblings[index + 1].keys) >= min_keys + 1):  # right
                    S = siblings[index + 1]
                
                if(S is not None): # S is either left or right sibling and it has extra entries
                    node.keys = node.keys[:idx] + node.keys[idx+1:]  # remove entry
                    node.values = node.values[:idx] + node.values[idx+1:] # remove values
                    if(left): # S is at left
                        lastKey = S.keys.pop()
                        lastValue = S.values.pop()

                        record_data = fileHandler.read_record(S.page_index, lastKey)
                        fileHandler.delete_record(S.page_index, lastKey)
                        fileHandler.write_record(node.page_index, record_data)

                        node.values.insert(0, lastValue)
                        node.keys.insert(0, lastKey)

                        node.parent.keys[index - 1] = lastKey
                    else:
                        firstKey = S.keys.pop(0)
                        firstValue = S.values.pop(0)

                        record_data = fileHandler.read_record(S.page_index, firstKey)
                        fileHandler.delete_record(S.page_index, firstKey)
                        fileHandler.write_record(node.page_index, record_data)

                        node.keys.append(firstKey)
                        node.values.append(firstValue)

                        node.parent.keys[index] = S.keys[0]  # for max degree = 3, min key = 1. We know that len(S.keys) > min + 1  
                    return None, True

                else:  # merge right node to left node - remove right node
                    node.keys = node.keys[:idx] + node.keys[idx+1:]  # delete the entry
                    node.values = node.values[:idx] + node.values[idx+1:] # remove values
                    if(index > 0): 
                        S = siblings[index - 1] # left
                        left = True
                    else: 
                        S = siblings[index + 1]          # right
                        left = False
                        
                    
                    if(left):   # S is on left, node is on right
                        idx_of_removed_child = index  # remove the right node
                        S.keys += node.keys # take all keys of node to S
                        S.values += node.values
                        S.nextNode = node.nextNode  # node is removed

                        fileHandler.merge_pages(S.page_index, node.page_index)

                        if(node.nextNode is not None): node.nextNode.previousNode = S


                    else:  # S is on right, node is on left
                        idx_of_removed_child = index + 1 # remove the right node
                        node.keys += S.keys
                        node.values += S.values
                        node.nextNode = S.nextNode

                        fileHandler.merge_pages(node.page_index, S.page_index)

                        if(S.nextNode is not None): S.nextNode.previousNode = node
                    
                    return idx_of_removed_child, True
        
    def BFS_extreme_verbose_test(self):
        # Return both keys and values   
        str_ = ""   
        if(self.root is None): 
            str_.append("Empty B+ Tree")
            return   
        queue = []
        queue.append(self.root)
        height = 0
        while(queue):
            size = len(queue)
            str_ += ("We are at the height:" + str(height) + " -- (key, value) pairs of nodes: \n")
            for _ in range(size):
                node = queue.pop(0)
                str_ += ("( [" + ", ".join([str(x) for x in node.keys]) + "]" + ", ".join([str(x) for x in node.values]))
                str_ += ("\n--------\n")
                a = None if node.previousNode is None else node.previousNode.keys
                b = None if node.nextNode is None else node.nextNode.keys
                c = None if node.parent is None else node.parent.keys
                str_ += ("keys of previous node: " + str(a) + "\n")
                str_ += ("keys of next node: " + str(b)+ "\n")
                str_ += ("keys of parent node: " + str(c)+ "\n")
                if(not node.isLeaf):
                    for child in node.values:
                        queue.append(child)
            str_ += ("\n")
            height += 1 
        return str_
                 
    def BFS_extreme_verbose(self):
        # Return both keys and values      
        if(self.root is None): 
            print("Empty B+ Tree")
            return   
        queue = []
        queue.append(self.root)
        height = 0
        while(queue):
            size = len(queue)
            print("We are at the height:", height, " -- (key, value) pairs of nodes: ", end = '')
            for _ in range(size):
                node = queue.pop(0)
                print("(", node.keys, node.values, ")--Parent=", node.parent,  sep="")
                print("--------")
                a = None if node.previousNode is None else node.previousNode.keys
                b = None if node.nextNode is None else node.nextNode.keys
                c = None if node.parent is None else node.parent.keys
                print("keys of previous node: ", a)
                print("keys of next node: ", b)
                print("keys of parent node: ", c)
                if(not node.isLeaf):
                    for child in node.values:
                        queue.append(child)
            print()
            height += 1                            
    
    def BFS(self):
        if(self.root is None): 
            print("Empty B+ Tree")
            return
        # Return only the keys for simplicity and readability.
        queue = []
        queue.append(self.root)
        height = 0
        while(queue):
            size = len(queue)
            print("We are at the height:", height, " -- Nodes: ", end = '')
            for _ in range(size):
                node = queue.pop(0)
                print("(", node.keys, "), page_id=", node.page_index, sep="", end="   ")
                if(not node.isLeaf):
                    for child in node.values:
                        queue.append(child)
            print()
            height += 1

    # opt = 1 --> looking for elements less than the key
    # opt = 2 --> looking for elements greater than the key
    def filter(self, opt, key):
        node = self.root
        while (not node.isLeaf):
            (index, child, onSpot) = self._find(node, key)

            if(onSpot): node = node.values[index + 1]
            else: node = child
        
        # now, we are at a leaf node

        if(opt == 2 and node.keys and node.keys[len(node.keys) - 1] <= key): node = node.nextNode
        elif(opt == 1 and node.keys and node.keys[0] >= key): node = node.previousNode

        nodes = []

        while(node != None):
            nodes.append(node)
            node = node.previousNode if opt == 1 else node.nextNode
                
        if len(nodes) == 1 and len(nodes[0].keys) == 0:
            return []
        else:
            return [node.page_index for node in nodes]
        


    def leaf_nodes(self):
        node = self.root

        nodes = []
        q = []
        q.append(node)
        while(q):
            node = q.pop(0)
            if(node.isLeaf): nodes.append(node)
            else: 
                for child in node.values:
                    q.append(child)

        if len(nodes) == 1 and len(nodes[0].keys) == 0:
            return []
        else:
            return [node.page_index for node in nodes]
