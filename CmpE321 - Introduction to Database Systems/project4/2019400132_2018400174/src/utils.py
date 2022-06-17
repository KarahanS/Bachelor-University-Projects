from bplustree import *
import json
from settings import settings

# As we change the structure of the node.values, we may have to update out helper functions for flatten and unflatten.

def flatten(node):
    if(node.isLeaf):
        return {
            "keys": node.keys,
            "page_index": node.page_index
        }
    else:
        #print(node.keys)
        return {
            "keys": node.keys,
            "children": [flatten(child) for child in node.values] 
        }


def unflatten(d, order):
    if('page_index' in d): # leaf node
        node = Node(order)
        node.keys = d['keys']
        node.values = [0] * len(d['keys'])
        node.page_index = d['page_index']
        return node
    else:
        node = Node(order)
        node.isLeaf = False
        node.keys = d['keys']

        for child in d['children']:
            ch = unflatten(child, order)
            ch.parent = node
            node.values.append(ch)
        return node

def link(node):
    queue = []
    queue.append(node)
    while(queue):
        size = len(queue)
        prev = None        
        for _ in range(size):
            node = queue.pop(0)
            
            if(not node.isLeaf):
                for child in node.values:
                    queue.append(child)

            node.previousNode = prev
            if(prev is not None): prev.nextNode = node
            prev = node

def to_json(file, tree):
    dict_ = flatten(tree.root)
    json_object = json.dumps(dict_, indent = 4)

    with open(file, "w") as outfile:
        outfile.write(json_object)

def from_json(file, order):
    try:
        with open(file, "r") as infile: 
            data = json.load(infile)
            tree = BPlusTree(order)

            node = unflatten(data, order)
            link(node)
            tree.root = node
            return tree
    except:
        print("File cannot be found.")
        return None

def move_item_within_list(l, f, t):
    temp = l[f]
    del l[f]
    l.insert(t, temp)
    return l

