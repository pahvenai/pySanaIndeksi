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
        self.lukija = lukija
        self.empty = RedBlackNode(None) # leaves are 'empty'
        self.root = self.empty
        self.root.parent = self.empty

    def add(self, object):
        '''
        Adds a new word to the tree.
        '''
#        newNode = self.binaryInsert(self.root, RedBlackNode(word))
#        self.insert1(newNode)
        word = object[0]
        pos = object[1:3]
        self.binaryInsert(RedBlackNode(word, pos))


    def find(self, word, type='startswith'):
        '''
        Tries to find the asked word from the tree. Returns a number indicating
        the file and a file number for each found instance. Can be used to find
        exact matches only.
        '''

        node = self.root
        while (not node == self.empty) and (not node.str == word):
            if word < node.str:
                node = node.le
            else:
                node = node.ri

        return node.pos

# def search(self, key, x=None):
#        """
#        Search the subtree rooted at x (or the root if not given) iteratively for the key.
#
#        @return: self.nil if it cannot find it.
#        """
#        if None == x:
#            x = self.root
#        while x != self.nil and key != x.key:
#            if key < x.key:
#                x = x.left
#            else:
#                x = x.right
#        return x







    def binaryInsert(self, node):

        if not self.root == self.empty:
            #find parent for node
            newParent = self.empty
            nextNode = self.root
            while nextNode != self.empty:
                newParent = nextNode
                print nextNode, node, self.root
                if node.str < nextNode.str:
                    nextNode = nextNode.le
                else:
                    nextNode = nextNode.ri
        else:
            newParent = self.root
        node.pa = newParent

        # empty tree: new node as root
        if newParent == self.empty:
            self.root = node
        elif node.str < newParent.str:
            newParent.le = node
        else:
            newParent.ri = node
        node.le = node.ri = self.empty # tree ends in empty nodes

        # node is set to red
        node.red = True
        # Red Black tree properties may not be intact, fix them from new node
        #self.restoreProperties(node)


    def restoreProperties(self, node):
        "Restore red-black properties after insert."

        # Two red nodes cannot follow each other
        while node.pa.red:
            uncle = node.uncle()
            if uncle == node.grandpa().ri:
                if uncle.red:
                    node.pa.red = False
                    uncle.red = False
                    node.grandpa().red = True
                    node = node.grandpa()
                else:
                    if node == node.pa.ri:
                        node = node.pa
                        self.leftRotate(node)
                    node.pa.red = False
                    node.grandpa().red = True
                    self.rightRotate(node.grandpa())
            else:
                if uncle.red:
                    node.pa.red = False
                    uncle.red = False
                    node.grandpa().red = True
                    node = node.grandpa()
                else:
                    if node == node.pa.le:
                        node = node.pa
                        self.rightRotate(node)
                    node.pa.red = False
                    node.grandpa().red = True
                    self.leftRotate(node.grandpa())
        self.root.red = False # root is black


    def leftRotate(self, node):
        """ Left rotate node """
        pivot = node.ri
        node.ri = pivot.le
        if pivot.le != self.empty:
            pivot.le.pa = node
        pivot.pa = node.pa
        if node.pa == self.empty:
            self.root = pivot
        elif node == node.pa.le:
            node.pa.le = pivot
        else:
            node.pa.ri = pivot
        pivot.le = node
        node.pa = pivot


    def rightRotate(self, node):
        """ Right rotate node """
        pivot = node.le
        node.le = pivot.ri
        if pivot.ri != self.empty:
            pivot.ri.pa = node
        pivot.pa = node.pa
        if node.pa == self.empty:
            self.root = pivot
        elif node == node.pa.ri:
            node.pa.ri = pivot
        else:
            node.p.le = pivot
        pivot.ri = node
        node.pa = pivot


class RedBlackNode(object):
    '''
    Contains the information of one branch.
    '''

    def __init__(self, str='', pos=None, pa=None, red=True):
        self.pa = pa
        self.le = None #left
        self.ri = None #right
        self.red = red
        self.str = str
        self.pos = pos
        if self.pos:
            self.empty = False
        else:
            self.empty = True

    def grandpa(self):
        if not self.pa.empty:
            return self.pa.pa
        else:
            return RedBlackNode()

    def uncle(self):
        grandpa = self.grandpa()
        if grandpa.empty:
            return RedBlackNode()
        elif grandpa.left == self.pa:
            return grandpa.right
        else:
            return grandpa.left

    def sibling(self):
        if self == self.pa.left:
            return self.pa.right
        else:
            return self.pa.left 

    def updateNode(self, object):
        pass
