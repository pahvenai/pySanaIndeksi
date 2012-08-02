from Puu import Puu

__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 17:35:35$"

if __name__ == "__main__":
    print "Contains a class for red-black tree"


class RedBlack(Puu):
    '''
    A Trie-type tree that can hold words containing alphanumerals and the '-'-
    character.

    NOTE: this is still a mess...
    '''



    def __init__(self, lukija):
        self.root = None
        self.lukija = lukija

    def add(self, word):
        '''
        Adds a new word to the tree.
        '''
        newNode = self.binaryInsert(self.root, RedBlackNode(word))
        self.insert1(newNode)

    def find(self, word, type='startswith'):
        '''
        Tries to find the asked word from the tree. Returns a number indicating
        the file and a file number for each found instance. Can be used to find
        exact matches only.
        '''
        pass


    def binaryInsert(self, oldNode, newNode):
        if oldNode == None:
            oldNode = newNode
            newNode.parent = oldNode
            return newNode
        elif newNode.str < oldNode.str:
            return self.binaryInsert(oldNode.left, newNode)
        else:
            return self.binaryInsert(newNode, oldNode.left)

    def insert1(self, node):
        if (node.parent == None):
            n.red = False
        else: self.insert2(node)

    def insert2(self, node):
        if not node.parent.red:
            return
        else: self.insert3(node)

    def insert3(self, node):
        u = node.uncle()
        if u and u.red:
            node.parent.red = False
            u.red = False
            g = node.grandpa()
            g.red = True
            self.insert1(g)
        else: self.insert4(node)

    def insert4(self, node):
        g = node.grandpa()
        if node == node.parent.right and node.parent == g.left:
            self.rotateLeft(node.parent)
            node = node.left
        elif node == node.parent.left and node.parent == g.right:
            self.rotateRight(node.parent)
            node = node.right
        self.insert5(node)

    def insert5(self, node):
        g = node.grandpa()
        node.parent.red = False
        g.red = True
        if node == node.parent.left:
            self.rotateRight(g)
        else:
            self.rotateLeft(g)

    def rotateLeft(self, node):
        r = node.right
        node.right = r.left
        if r.left:
            r.left.parent = node
        r.parent = node.parent
        if not node.parent:
            self.root = r
        elif node == x.parent.left:
            x.parent.left = r
        else:
            x.parent.right = r
        r.left = node
        node.parent = r

    def rotateRight(self, node):
        l = node.left
        node.left = l.right
        if l.right:
            l.right.parent = node
        l.parent = node.parent
        if not node.parent:
            self.root = l
        elif node == x.parent.right:
            x.parent.right = l
        else:
            x.parent.left = l
        l.right = node
        node.parent = l


class RedBlackNode(object):
    '''
    Contains the information of one branch.
    '''

    def __init__(self, object, parent=None, red=True):
        self.exact = []
        self.parent = parent
        self.left = None
        self.right = None
        self.red = red
        self.str = object[0]
        self.pos = object[1:3]

    def grandpa(self):
        if not self.parent == None:
            return self.parent.parent
        else:
            return None

    def uncle(self):
        grandpa = self.grandpa()
        if grandpa == None:
            return None
        elif grandpa.left == self.parent:
            return grandpa.right
        else:
            return grandpa.left

    def sibling(self):
        if self == self.parent.left:
            return self.parent.right
        else:
            return self.parent.left 

    def updateNode(self, object):
        pass