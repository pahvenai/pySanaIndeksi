# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 18:12:31$"

# tools for creating an abstract class in python
from abc import ABCMeta, abstractmethod, abstractproperty

if __name__ == "__main__":
    print "This is an abstract class, implemented with the abc class"

class Tree(object):
    __metaclass__ = ABCMeta
    """
    This is an abstract class. Classes that inherit from this class should have
    implementation for adding an item to a tree and finding an item from a tree.
    This class is not strictly speaking necessary but it makes sure your tree
    classes are working properly.

    Guarantees that the following properties and methods have been defined:
    properties:
    wordCount:  number of words added to the tree (not number of nodes)
    type:       finds 'exact' or 'partial' matches for words
    public methods:
    self.add(key, value):   Adds one value with the given key to the tree
    self.addFromReader():   Adds words from own reader if possible
    self.clear():           Removes all words from the tree
    self.find(key):         Returns the hits when searching for key
    """

##################
### PROPERTIES ###
##################

    @abstractproperty
    def wordCount(self):
        raise NotImplementedError( "WordCount not implemented" )

    @abstractproperty
    def type(self):
        raise NotImplementedError( "Type not implemented" )

######################
### PUBLIC METHODS ###
######################

    @abstractmethod
    def add(self, key, value):
        """
        This method is used to add items to the tree. Each item contains a key
        which should be a string and an arbitrary value corresponding to that
        key.

        @param key: the key to the value to be added
        @param value: the value to be added
        """
        raise NotImplementedError( "Adding not implemented" )

    @abstractmethod
    def addFromReader(self, wordCount = None):
        """
        This method should take the words from self.lukija and add them to the
        tree. If wordCount is given this method should not increase the number
        of additions to the tree over wordCount. Note that the actual number of
        unique words in the tree does not equal wordCount.

        @param wordCount: the maximum number of words added to the tree
        """
        raise NotImplementedError( "Adding from reader not implemented" )

    @abstractmethod
    def clear(self):
        """
        This method is used to clear all the words from the tree.
        """
        raise NotImplementedError( "Clearing not implemented" )

    @abstractmethod
    def find(self, key, output='list', sanitized=False):
        """
        Finds the key from the tree. Word is first sanitized unless sanitized is
        set to True.
        
        @param key: the key for the value to be found
        @param output: the type of output desired
        @type output: boolean
        @param sanitized: if set to True words are assumed to be sanitized
        @type sanitized: boolean
        
        @return:
            - output == 'boolean':
                1:  A boolean value indicating whether the file was found
            - output == 'count':
                1:  Number of found instances
            - output == 'full':
                1:  A list of positions where this word was found
                2:  Number of found instances
                3:  Number of lines where the word was found
            - output == 'list': (default)
                1:  A list of positions where this word was found
        """
        raise NotImplementedError( "Finding not implemented" )

