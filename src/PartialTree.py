# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$13.8.2012 14:01:02$"

# tools for creating an abstract class in python
from abc import ABCMeta, abstractmethod
from Tree import Tree

if __name__ == "__main__":
    print "This is an abstract class, implemented with the abc class"

class PartialTree(Tree):
    __metaclass__ = ABCMeta

    _type = 'partial' # tag for partial trees

    @abstractmethod
    def findPartial(self, key, output='list'):
        """
        Finds the key from the tree
        If the key is found return the following:
        output == 'list';
        1:  A list of positions where this word was found
        output == 'count':
        1:  Number of found instances
        2:  Number of lines where the word was found
        output == 'full';
        1:  A list of positions where this word was found
        2:  Number of found instances
        3:  Number of lines where the word was found
        """
        raise NotImplementedError( "Partial finding not implemented" )