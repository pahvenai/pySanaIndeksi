# To change this template, choose Tools | Templates
# and open the template in the editor.

from Puu import Puu

__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 12:16:17$"

if __name__ == "__main__":
    print "Contains a class for Trie-tree"


class Trie(Puu):
    '''
    A Trie-type tree that can hold words containing alphanumerals and the '-'-
    character.
    '''



    def __init__(self):
        self.root = None

    def add(self, word):
        '''
        Adds a new word to the tree.
        '''
        pass

    def find(self, word, type='startswith'):
        '''
        Tries to find the asked word from the tree. Returns a number indicating
        the file and a file number for each found instance. Can be used to find
        exact matches or the beginnings of the words. 
        '''

        pass


class TrieBranch(object):
    '''
    Contains the information of one branch.
    '''

    NO_DIFF_CHARS = 50

    def __init__(self):
        self.exact = []
        self.match = []
        self.children = [None] * NO_DIFF_CHARS

