# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$13.8.2012 14:01:02$"

# tools for creating an abstract class in python
from abc import ABCMeta, abstractmethod
# This inherits from another abstract class
from Tree import Tree

if __name__ == "__main__":
    print "This is an abstract class, implemented with the ABCMeta class"

class PartialTree(Tree):
    __metaclass__ = ABCMeta

    _type = 'partial' # tag for partial trees

    @abstractmethod
    def findPartial(self, key, output='list'):
        """
        Finds the key from the tree. Return type defined by param output

        @param key: The key to be found
        @param output: the type of output desired
        @type output: string

        @return:
            - output == 'boolean':
                1:  A boolean value indicating whether the file was found
            - output == 'count':
                1:  Number of found instances
                2:  Number of lines where the word was found
            - output == 'full':
                1:  A list of positions where this word was found
                2:  Number of found instances
                3:  Number of lines where the word was found
            - output == 'list': (default)
                1:  A list of positions where this word was found
        """
        raise NotImplementedError( "Partial finding not implemented" )