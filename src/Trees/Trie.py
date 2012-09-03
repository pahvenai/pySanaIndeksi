# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 12:16:17$"

# Path hack.
import sys; import os; sys.path.insert(0, os.path.abspath('..'))

from PartialTree import PartialTree
from Support.LinkedList import LinkedList
import random

if __name__ == "__main__":
    print "Contains a class for Trie-tree"


class Trie(PartialTree):
    '''
    A Trie-type tree that can hold words containing alphanumerals, hyphens and
    aposthrophes. The WordReader module handles in reality the the word
    sanitizing.

    A trie instance is tied to its WordReader object: it gets the size of the
    child node list from it and the mapping of characters to indices in that
    list.
    
    The value of the trie node is determined by traversing from root to the 
    node. Each trie node holds two lists: one for positions where an exact match
    is found (if any) and one for all words that start with those letters. That
    it way it is a PartialTree.

    properties:
    wordCount:  number of words added to the tree (not number of nodes)
    type:       finds 'exact' or 'partial' matches for words according to type
    public methods:
    add(key, value):    Adds one value with the given key to the tree
    clear():            Removes all words from the tree
    find(key):          Returns the hits when searching for key
    findPartial(key):   Finds hits for keywords starting with key
    addFromReader():    Adds words from own reader if possible
    printRandomRoute(): Prints a random route from root to leaf.
    private methods:
    _addNode(key, value): Recursively adds each letter in the key to the tree
                          (in correct place) and adds value to each node
    _find(word):          Handles mainly the type of output and calls _findRe...
    _findRecursive(word, charNo, type, node):
                          Traverses the tree to find (if possible) the word
    '''


    def __init__(self, wordreader):
        self.lukija = wordreader
        self.charMapSize = self.lukija.getCharMapSize()
        self.clear()

##################
### PROPERTIES ###
##################

    @property
    def wordCount(self):
        """ number of words added to the tree (not number of nodes) """
        return self._wordCount

    @property
    def type(self):
        """ finds 'exact' or 'partial' matches for words according to type """
        return self._type # _type 'partial' given in PartialTree class

######################
### PUBLIC METHODS ###
######################

    def add(self, key, value):
        '''
        Adds a new value to the tree. The addition is done via recursive addNode
        function. The value is stored using the key.

        @param key: the key to the value to be added
        @param value: the value to be added
        '''
        key = self.lukija.sanitize(key)
        if not key:
            return None # can't add empty keys
        self._wordCount = self._wordCount + 1
        if self.root == None:
            self.root = TrieNode(self.charMapSize)
        self._addNode(key, value)

    def addFromReader(self, wordCount = None):
        """
        Adds all the words in the WordReader object to this tree.

        @param wordCount: maximum number of words read from reader
        @type wordCount: integer
        """
        if self.lukija:
            for item in self.lukija.words:
                self.add(item[0], item[1:])
                if wordCount and self.wordCount() == wordCount:
                    break

    def clear(self):
        """ Clears all words from the tree """
        self.root = None
        self._wordCount = 0

    def find(self, word, output='full', sanitized=False):
        """
        Finds the word in this tree using intenal self._find method.
        Output options are listed in super class Tree in method find.
        The optional sanitized flag can be used if input is known to
        be sanitized already. Do not use it for non-sanitized input.

        @param word: the word to be found
        @type word: string
        @param output: the type of output desired
        @type output: boolean
        @param sanitized: if set to True words are assumed to be sanitized
        @type sanitized: boolean
        """
        if self.wordCount == 0:
            return None
        return self._find(word, 'exact', output, sanitized)

    def findPartial(self, word, output='full', sanitized=False):
        """
        Finds the keys beginning with word in this tree using intenal self._find
        method. Output options are listed in super class Tree in method find.
        The optional sanitized flag can be used if input is known to
        be sanitized already. Do not use it for non-sanitized input.

        @param word: the word to be found
        @type word: string
        @param output: the type of output desired
        @type output: boolean
        @param sanitized: if set to True words are assumed to be sanitized
        @type sanitized: boolean
        """
        if self.wordCount == 0:
            return None
        return self._find(word, 'partial', output, sanitized)

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
                        lastindex = random.choice(indices) # randomization here!
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
        Add one node at a time until the whole word is added. Each node
        represents a letter of that word.
        charNo tells which index of key we are adding.
        '''
        letter = key[charNo]
        index = self.lukija.idxMap[letter]

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



    def _find(self, word, type='partial', output='full', sanitized=False):
        '''
        Tries to find the asked word from the tree. Can be used to find
        exact matches or the beginnings of the words. Uses recursion to travel
        in the trie-tree. Returns a list of the positions where that word was
        found (if any), the number of found instances and the number of
        different line where that word was found.

        The word is first sanitized unless sanitized flag is up.
        '''
        if not sanitized:
            word = self.lukija.sanitize(word) # check that we have no illegal characters
        # find this word in the tree recursively and return positions of all the
        # instances
        if output == 'boolean':
            return self._findRecursive(word, 1, type, self.root, boolean=True)
        positions = self._findRecursive(word, 1, type, self.root)
        if output == 'list':
            return positions

        if positions: #found
            count = len(positions)
            linecount = len(set(positions))
        else: #did not find the word
            count = 0; linecount = 0;

        if output == 'count':
            return count
        elif output == 'full':
            return positions, count, linecount
        else:
            return None



    def _findRecursive(self, word, charNo, type, node, boolean=False):
        """
        First we check that a required letter exist in the tree. If not, we did
        not find the word. If we find it and it's the last letter to find,
        return the instances where this word was found. If it's not the last
        letter move on recursively to the next letter.
        """
        char = word[charNo-1]
        index = self.lukija.idxMap[char]

        if not node.children[index]:
            return None # Required letter not found
        else:
            # if the next letter is the last letter, we found our letter
            if charNo == len(word):
                if boolean:
                    return True
                if type == 'exact':
                    return node.children[index].exact.values()
                else:
                    return node.children[index].match.values()

            return self._findRecursive(word, charNo+1, type, node.children[index], boolean)







class TrieNode(object):
    '''
    Contains the information of one node. It contains two lists of the positions
    where the string corresponding to that node is found. One stores only the
    positions of exact matches and the other all words that start with that
    string (match).

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
        self.children = [None] * charMapSize


    def updateNode(self, position, exact):
        """ Add position info for this object """
        self.match.addLast(position)
        if exact:
            self.exact.addLast(position)