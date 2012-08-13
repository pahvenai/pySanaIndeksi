# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 12:16:17$"

from PartialTree import PartialTree
from WordReader import WordReader
from LinkedList import LinkedList
import random

if __name__ == "__main__":
    print "Contains a class for Trie-tree"

# egrep "( sana|^sana)" *.txt -i --count
# egrep "( sana|^sana)" *.txt -ni

class Trie(PartialTree):
    '''
    A Trie-type tree that can hold words containing alphanumerals, hyphens and
    aposthrophes. The WordReader module handles in reality the the word
    sanitizing.

    A trie instance is tied to its WordReader object: it gets the size of the
    child node list from it and the mapping of characters to indices in that
    list.

    properties
    wordCount:  number of words added to the tree (not number of nodes)
    type:       finds 'exact' or 'partial' matches for words
    methods:
    self.add(key, value):   Adds one value with the given key to the tree
    self.clear():           Removes all words from the tree
    self.find(key):         Returns the hits when searching for key
    self.findPartiale(key): Finds hits for keywords starting with key
    self.addFromReader():   Adds words from own reader if possible
    self.printRandomRoute():Prints a random route from root to leaf.
    '''


    def __init__(self, wordreader):
        self.lukija = wordreader
        self.charMapSize = self.lukija.getCharMapSize()
        self.clear()

##################
### PROPERTIES ###
##################

    def wordCount(self):
        return self._wordCount

    def type(self):
        return self._type # type given in PartialTree class

###############
### METHODS ###
###############

    def add(self, key, value):
        '''
        Adds a new word to the tree. The addition is done via recursive addNode
        function.
        '''
        key = self.lukija.sanitize(key)
        if not key:
            return None
        self._wordCount = self.wordCount() + 1
        if self.root == None:
            self.root = TrieNode(self.charMapSize)
        self._addNode(key, value)

    def addFromReader(self, wordCount = None):
        """ Adds all the words in the WordReader object to this tree """
        if self.lukija:
            for item in self.lukija.words:
                self.add(item[0], item[1:])
                if wordCount and self.wordCount() == wordCount:
                    break

    def clear(self):
        """ Clears all words from the tree """
        self.root = None
        self._wordCount = 0

    def find(self, word, output='full'):
        return self._find(word, 'exact', output)

    def findPartial(self, word, output='full'):
        return self._find(word, 'partial', output)

    def printRandomRoute(self):
        """
        Prints a random route from root to leaf.
        """

        parent = self.root
        word = ''
        lastindex = None
        while(True):
            if not parent == None:
                if parent.children:
                    lastindex = None
                    indices = []
                    for index, child in enumerate(parent.children):
                        if child:
                            print word + self.lukija.ind2char(index),
                            indices.append(index)
                            lastindex = index
                    if lastindex == None:
                        break
                    else:
                        lastindex = random.choice(indices)
                        parent = parent.children[lastindex]
                    print '; route: ', self.lukija.ind2char(lastindex), ' found n=', \
                          parent.match.count, ' (', len(set(parent.match.values())), \
                          'lines) @ ', parent.match.values()
                    word = word + self.lukija.ind2char(lastindex)

#######################
### PRIVATE METHODS ###
#######################

    def _addNode(self, key, value, charNo = 0, node = 'root'):
        '''
        Add a node at a time until the whole word is added. Each node represents
        a letter of that word.
        '''
        letter = key[charNo]
        index = self.lukija.char2ind(letter)

        if node == 'root':
            node = self.root

        exact = False
        if charNo == len(key) - 1:
            exact = True

        nodeExists = node.children[index] # Empty list means no such node

        if nodeExists:
            # node exists, update only the newly found position to the node
            nodeExists.updateNode(value, exact)
            nextNode = node.children[index] # tree may continue here
        else:
            # create a new branch and add it to the tree
            newNode = TrieNode(self.charMapSize, value, exact)
            node.children[index] = newNode
            nextNode = newNode # tree may continue here

        # If not the last letter in the word, continue recursively
        if not exact:
            charNo = charNo + 1
            self._addNode(key, value ,charNo,nextNode)
        pass



    def _find(self, word, type='partial', output='full'):
        '''
        Tries to find the asked word from the tree. Can be used to find
        exact matches or the beginnings of the words. Uses recursion to travel
        in the trie-tree. Returns a list of the positions where that word was
        found (if any), the number of found instances and the number of
        different line where that word was found.

        The word is first sanitized.
        '''

        word = self.lukija.sanitize(word) # check that we have no illegal characters
        # find this word in the tree recursively and return positions of all the
        # instances
        positions = self._findRecursive(word, 1, type, self.root)

        if positions: #found
            count = len(positions)
            linecount = len(set(positions))
        else: #did not find the word
            count = 0; linecount = 0

        if output == 'list':
            return positions
        elif output == 'count':
            return count
        elif output == 'full':
            return positions, count, linecount
        else:
            return None



    def _findRecursive(self, word, charNo, type, node):
        """
        First we check that a required letter exist in the tree. If not, we did
        not find the word. If we find it and it's the last letter to find,
        return the instances where this word was found. If it's not the last
        letter move on recursively to the next letter.
        """
        char = word[charNo-1]
        index = self.lukija.char2ind(char)

        if not node.children[index]:
            return None # Required letter not found
        else:
            # if the next letter is the last letter, we found our letter
            if charNo == len(word):
                if type == 'exact':
                    return node.children[index].exact.values()
                else:
                    return node.children[index].match.values()

            return self._findRecursive(word, charNo+1, type, node.children[index])







class TrieNode(object):
    '''
    Contains the information of one node. It contains two lists of the positions
    where the string corresponding to that node is found. One stores only the
    positions of exact matches and the other all words that start with that
    string.

    Child maintenance is handled with a minimum list. A new TrieNode is given
    the maximum amount of children (number of acceptable characters).

    self.updateNode(value, exact):
        Adds the value to the value lists of that node. Exact-flag determines
        whether the value is added also to the list of exact matches.
    '''

    def __init__(self, charMapSize, value = '', exact = False):
        """
        Trie node contains two linked lists for its values: one is intended for
        exact matches (it is updated only with exact-flag raised). Upon
        creation, the minimum list type child list is created for that node.
        """
        self.exact = LinkedList()
        self.match = LinkedList()
        if value:
            self.updateNode(value, exact)
        self.children = [None] * (charMapSize)


    def updateNode(self, position, exact):
        """ Add position info for this object """
        self.match.addLast(position)
        if exact:
            self.exact.addLast(position)