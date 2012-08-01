# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 12:16:17$"

if __name__ == "__main__":
    print "Contains classes for trees"


class Trie(object):
    '''
    A Trie-type tree that can hold words containing alphanumerals and the '-'-
    character.
    '''
    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def add(self, word):
        '''
        Adds a new word to the tree.
        '''
        pass
    def remove(self, word):
        '''
        Removes a word from the tree, if it exists.
        '''
        pass
    def find(self, word, type='startswith'):
        pass
    