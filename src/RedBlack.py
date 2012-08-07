# -*- coding: utf-8 -*-
from Puu import Puu
from LinkedList import LinkedList
from sys import stdout

__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 17:35:35$"

if __name__ == "__main__":
    print "Contains a class for red-black tree"


class RedBlack(Puu):
    '''
    A Trie-type tree that can hold words containing characters. The WordReader
    is optional, it can be passed to facilitate reading words from it.

    The tree is initially empty. The leaves are always empty black nodes.

    methods:
    self.clear:
    '''



    def __init__(self, lukija=None):
        """ Only empty trees can be created. WordReader object is optional. """
        self.lukija = lukija
        self.clear()

    def clear(self):
        """ Gets rid of all the nodes in the tree (if any) """
        self.empty = RedBlackNode(None) # leaves are 'empty'
        self.root = self.empty
        self.root.parent = self.empty

    def add(self, key, value):
        '''
        Adds a new word to the tree. Adding is done with binaryInsert, which
        calls for a function that restores the tree to red and black if the
        addition of this word damaged those properties.
        '''
        self.binaryInsert(RedBlackNode(key, value), value)

    def addFromReader(self):
        """ Adds all the words in the WordReader object to this tree """
        if self.lukija:
            for item in self.lukija.words:
                self.add(item[0], item[1:])

    def find(self, key):
        '''
        Calls an internal function which does the actual finding.
        '''
        key = self.lukija.sanitize(key)
        _, values, itemCount, RowCount = self._internalFind(key, type)
        return values, itemCount, RowCount



    def _internalFind(self, word, type='startswith'):
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

        if not node.key == word:
            return self.empty, [], 0, 0
        vals = node.val.values()
        return node, vals, len(vals), len(set(vals))


    def binaryInsert(self, node, value=None):
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

#        if newParent.key == node.key: # if node already exists ...
#            newParent.updateNode(value) # ... just update its value
#            return

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


    def _restoreProperties(self, node):
        """
        This restores the Red Black tress properties so that the tree remains
        balanced. There are six different cases and some require more fixing
        than others. Left (and right) rotation are done in help routines.
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


    def _leftRotate(self, node):
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


    def _rightRotate(self, node):
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
            node.pa.le = pivot
        pivot.ri = node
        node.pa = pivot

def dotWrite(tree, out = stdout, showNone=False):
    "Write the tree in the dot language format to f."
    def nodeID(node):
        return 'N%d' % id(node)

    def nodeColor(node):
        if node.red:
            return "red"
        else:
            return "black"

    def visitNode(node):
        "Visit a node."
        print >> out, "  %s [label=\"%s\", color=\"%s\"];" % (nodeID(node), node, nodeColor(node))
        if node.le:
            if node.le != tree.empty or showNone:
                visitNode(node.le)
                print >> out, "  %s -> %s ;" % (nodeID(node), nodeID(node.le))
        if node.ri:
            if node.ri != tree.empty or showNone:
                visitNode(node.ri)
                print >> out, "  %s -> %s ;" % (nodeID(node), nodeID(node.ri))

    print >> out, "// Created by rbtree.write_dot()"
    print >> out, "digraph red_black_tree {"
    visitNode(tree.root)
    print >> out, "}"


class RedBlackNode(object):
    '''
    Contains the information of one branch.
    The node knows its children (le[ft] and ri[ght]), its pa[rent], its color,
    its key and its val[ue]. It also knows if it's empty (end-of-list-marker).
    Note that nodes cannot store empty values.

    Nodes know their family through
    methods:
    self.updateNode(val):   Add the val(ue) to this node
    self.grandpa():         return the grandpa node or empty node
    self.uncle():           return the uncle node or empty node
    self.sibling():         return the sibling node
    '''

    def __init__(self, str='', val=None, pa=None, red=True):
        """ The node can be empty upon creation (if val is not given) """
        self.pa = pa
        self.le = None #left
        self.ri = None #right
        self.red = red
        self.key = str
        self.val = LinkedList()
        if val:
            self.empty = False
            self.updateNode(val)
        else:
            self.empty = True

    def updateNode(self, value):
        """ Add the value to this node """
        self.val.addLast(value)

    def grandpa(self):
        """ Return the parent of a parent or empty node """
        if not self.pa.empty:
            return self.pa.pa
        else:
            return RedBlackNode()

    def uncle(self):
        """ Return the sibling of the parent or empty node """
        grandpa = self.grandpa()
        if grandpa.empty:
            return RedBlackNode()
        elif grandpa.le == self.pa:
            return grandpa.ri
        else:
            return grandpa.le

    def sibling(self):
        """ Return the sibling of the node (it must exist) """
        if self == self.pa.le:
            return self.pa.ri
        else:
            return self.pa.le 



    def __str__(self):
        "String representation."
        return str(self.key)


    def __repr__(self):
        "String representation."
        return str(self.key)