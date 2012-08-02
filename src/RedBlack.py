from Puu import Puu

__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 17:35:35$"

if __name__ == "__main__":
    print "Contains a class for red-black tree"


class RedBlack(Puu):
    '''
    A Trie-type tree that can hold words containing alphanumerals and the '-'-
    character.
    '''



    def __init__(self, lukija):
        self.root = None
        self.lukija = lukija

    def add(self, word):
        '''
        Adds a new word to the tree.
        '''
        pass

    def find(self, word, type='startswith'):
        '''
        Tries to find the asked word from the tree. Returns a number indicating
        the file and a file number for each found instance. Can be used to find
        exact matches only.
        '''
        pass


class RedBlackBranch(object):
    '''
    Contains the information of one branch.
    '''

    NO_DIFF_CHARS = 50

    def __init__(self, parent, red=True):
        self.exact = []
        self.parent = parent
        self.left = None
        self.right = None
        self.red = red

    def grandparent(self):
        if not self.parent == None:
            return self.parent.parent
        else:
            return None

    def uncle(self):
        grandpa = self.grandparent()
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
