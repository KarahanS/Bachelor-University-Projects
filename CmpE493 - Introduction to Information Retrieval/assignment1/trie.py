class Pair:
    def __init__(self):
        self.first = 0
        self.second = []
    def __repr__(self):
        return "({}, {})".format(self.first, self.second)

# We do not need to explicitly sort the dictionary - because we will be providing the document IDs and positions in order
class Posting:
    def __init__(self, word):
        self.word = word
        self.index = {} # dictionary
    
    def insert(self, docID, position):
        if docID in self.index:
            self.index[docID].first += 1
            self.index[docID].second.append(position) # positions are not ordered
        else:
            self.index[docID] = Pair()
            self.index[docID].first = 1
            self.index[docID].second.append(position)

    
    def __repr__(self):
        return "word: {}".format(self.word) + "\n" + "document frequency: {}".format(self.document_freq) + "\n" + self.index.__repr__()


# represents vocabulary using trie data structure
class Trie():
    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word: str, docID: int, position: int):
        node = self.root

        for char in word:
            if char in node.children: # check if char is one of the children
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.is_end = True
        if(node.posting is None): # first time being created
            node.posting = Posting(word)
        
        node.posting.insert(docID, position)
    
    def search(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return False
        return node.posting
        


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = {} # a dictionary of characters-TrieNodes
        self.is_end = False
        self.posting = None


if __name__ == "__main__":
    tr = Trie()
    tr.insert("here", docID = 1, position = 30)
    tr.insert("here", docID = 4, position = 12)
    tr.insert("he", docID = 2, position = 5)
    tr.insert("hello", docID = 2, position = 7)
    tr.insert("how", docID = 3, position = 24)
    tr.insert("her", docID = 1, position = 21)
    tr.insert("here", docID = 4, position = 5)
    tr.insert("here", docID = 3, position = 6)

    n3 = tr.search("here")
    print(n3.is_end)
