# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 17:35:35$"

from Tree import Tree
from LinkedList import LinkedList
from sys import stdout


if __name__ == "__main__":
    print "Contains a class for red-black tree"


class RedBlack(Tree):
    '''
    A Trie-type tree that can hold words containing characters. The WordReader
    is optional, it can be passed to facilitate reading words from it.

    The tree is initially empty. The leaves are always empty black nodes.

    All nodes are from class RedBlackNode.

    These properties and methods are defined by Tree class:
    properties:
    type:       type of searches stored; value is 'exact'
    wordCount:  number of words added to the tree (not number of nodes)
    public methods:
    add(key, value):   Adds one value with the given key to the tree
    addFromReader():   Adds words from own reader if possible
    clear():           Removes all words from the tree
    find(key):         Returns the hits when searching for key
    private methods:
    _binaryInsert(self, node):  Insert this value and when done, restore RB-tree
    _internalFind(word):        Find the word in the tree, if it exists
    _leftRotate(node):          Do a left-rotate for this node
    _restoreProperties(node):   Starting from node, restore RB-tree
    _rightRotate(node):         Do a right-rotate for this node
    '''

    def __init__(self, lukija=None):
        """ Only empty trees can be created. WordReader object is optional. """
        self.lukija = lukija
        self._type = 'exact'
        self.clear()

##################
### PROPERTIES ###
##################

    def type(self):
        return self._type

    def wordCount(self):
        return self._wordCount

######################
### PUBLIC METHODS ###
######################

    def add(self, key, value):
        '''
        Adds a new word to the tree. Adding is done with binaryInsert, which
        calls for a function that restores the tree to red and black if the
        addition of this word damaged those properties.
        '''
        key = self.lukija.sanitize(key)
        if key:
            self._wordCount = self.wordCount() + 1
            self._binaryInsert(RedBlackNode(key, value), value)

    def addFromReader(self, wordCount = None):
        """ Adds all the words in the WordReader object to this tree """
        if self.lukija:
            for item in self.lukija.words:
                self.add(item[0], item[1:])
                if wordCount and self.wordCount() == wordCount:
                    break

    def clear(self):
        """ Gets rid of all the nodes in the tree (if any) """
        self.empty = RedBlackNode(None) # leaves are 'empty'
        self.root = self.empty
        self.root.parent = self.empty
        self._wordCount = 0


    def find(self, key, output='full', sanitized=False):
        '''
        Calls an internal function which does the actual finding.

        The word is first sanitized.
        '''
        if self.wordCount() == 0:
            return None
        if not sanitized:
            key = self.lukija.sanitize(key)
        if output == 'boolean':
            return self._internalFind(key, boolean=True)
        _, values, itemCount, RowCount = self._internalFind(key)
        if output == 'list':
            return values
        elif output == 'count':
            return itemCount
        elif output == 'full':
            return values, itemCount, RowCount
        else:
            return None

#######################
### PRIVATE METHODS ###
#######################

    def _binaryInsert(self, node, value=None):
        """
        First add node as in a regular non-balanced binary tree. Then fix the
        binary tree to be a balanced Red Black tree.
        """

        if not self.root == self.empty:
            if self.root.key == node.key: # special case: update root
                self.root.val.addLast(value)
                return
            #find parent for node
            newParent = self.empty
            nextNode = self.root
            while nextNode != self.empty:
                newParent = nextNode
                if node.key == nextNode.key: # if node already exists ...
                    nextNode.updateNode(value) # ... just update its value
                    return
                elif node.key < nextNode.key:
                    nextNode = nextNode.le
                else:
                    nextNode = nextNode.ri
        else:
            newParent = self.root

        node.pa = newParent

        # update parent's child
        if newParent == self.empty: # empty tree: new node as root
            self.root = node
        elif node.key < newParent.key:
            newParent.le = node
        else:
            newParent.ri = node
        node.le = node.ri = self.empty # tree ends in empty nodes

        # node is set to red
        node.red = True
        # Red Black tree properties may not be intact, fix them from new node
        self._restoreProperties(node)

    def _internalFind(self, word, boolean=False):
        """
        Tries to find the asked word from the tree. Can be used to find
        exact matches only. Returns the node where that word was found, the
        positions where the word were found, number of found instances and the
        number of different lines where the word was found.
        """
        node = self.root
        while (not node == self.empty) and (not node.key == word):
            if word < node.key:
                node = node.le
            else:
                node = node.ri

        if boolean:
            if not node.key == word:
                return False
            else:
                return True
        if not node.key == word:
            return self.empty, [], 0, 0
        vals = node.val.values()
        return node, vals, len(vals), len(set(vals))

    def _leftRotate(self, node):
        """
        Left rotate node

        Algorithm modified from: 
        http://code.activestate.com/recipes/576817-red-black-tree/
        John Reid, Jun 20, 2009
        originally from "Introduction to Algorithms" by Cormen et al.
        """
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

    def _restoreProperties(self, node):
        """
        This restores the Red Black tree's properties so that the tree remains
        balanced. There are six different cases (and some require more fixing
        than others). Left (and right) rotation are done in help routines.
        """

        pa = node.pa
        # Two red nodes cannot follow each other
        while pa and pa.red:
            uncle = node.uncle()
            grandpa = node.grandpa()
            if uncle == grandpa.ri:
                if uncle.red:
                    pa.red = False
                    uncle.red = False
                    grandpa.red = True
                    node = grandpa
                else:
                    if node == pa.ri:
                        node = pa
                        self._leftRotate(node)
                    pa.red = False
                    grandpa.red = True
                    self._rightRotate(grandpa)
            else:
                if uncle.red:
                    pa.red = False
                    uncle.red = False
                    grandpa.red = True
                    node = grandpa
                else:
                    if node == pa.le:
                        node = pa
                        self._rightRotate(node)
                    pa.red = False
                    grandpa.red = True
                    self._leftRotate(grandpa)
        self.root.red = False # root is black

    def _rightRotate(self, node):
        """
        Right rotate node

        Algorithm modified from: 
        http://code.activestate.com/recipes/576817-red-black-tree/
        John Reid, Jun 20, 2009
        originally from "Introduction to Algorithms" by Cormen et al.
        """
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
            node.pa.le = pivot
        pivot.ri = node
        node.pa = pivot



class RedBlackNode(object):
    '''
    Contains the information of one branch.
    The node knows its children (le[ft] and ri[ght]), its pa[rent], its color,
    its key and its val[ue]. It also knows if it's empty (end-of-list flag).
    Note that nodes cannot store empty values.

    Nodes know their family through the following methods
    methods:
    grandpa():         return the grandpa node or empty node
    sibling():         return the sibling node
    uncle():           return the uncle node or empty node
    updateNode(val):   Add the val(ue) to this node
    '''

    def __init__(self, str='', val=None, pa=None, red=True):
        """ The node can be empty upon creation (if val is not given) """
        self.pa = pa
        self.le = None #left child
        self.ri = None #right child
        self.red = red
        self.key = str
        self.val = LinkedList()
        if val:
            self.empty = False
            self.updateNode(val)
        else:
            self.empty = True

    def __str__(self):
        """ String representation: return key as string """
        return str(self.key)

    def __repr__(self):
        """ String representation: return key as string """
        return str(self.key)

    def grandpa(self):
        """ Return the parent of a parent or empty node """
        if not self.pa.empty:
            return self.pa.pa
        else:
            return RedBlackNode()

    def sibling(self):
        """ Return the sibling of the node (it must exist) """
        if self == self.pa.le:
            return self.pa.ri
        else:
            return self.pa.le

    def uncle(self):
        """ Return the sibling of the parent or empty node """
        grandpa = self.grandpa()
        if grandpa.empty:
            return RedBlackNode()
        elif grandpa.le == self.pa:
            return grandpa.ri
        else:
            return grandpa.le

    def updateNode(self, value):
        """ Add the value to this node """
        self.val.addLast(value)

