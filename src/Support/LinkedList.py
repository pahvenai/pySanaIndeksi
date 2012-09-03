# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$6.8.2012 13:26:52$"

if __name__ == "__main__":
    print "This module contains a simple linked list class"


class LinkedList(object):
    """
    A simple doubly linked list class that provides three public methods; one
    for adding an item at the end of the list, one for retrieving the last item
    in the list and one for retrieving a list of all of the values stored in
    that list. Includes a counter for the number of items in the list. The list
    can also be cleared. Nodes are instances of class LinkedListNode.

    properties:
    count:         Returns the number of items in this list (number of nodes).
    public methods:
    clear():       Clears the list
    addLast(value):Adds the value to the end of the list.
    removeLast():  Removes the last value in the list and returns its value
    values():      Retrieve a list of all values in the linked list.
    """


    def __init__(self):
        """ Can only be used to create an empty list """
        self.clear()

    @property
    def count(self):
        """ The number of items in this list (number of nodes) """
        return self._count

    def addLast(self, value):
        """
        Add one value to the end of the list
        @param value: the value to be added to the list
        @type value: any valid python object
        """
        newNode = LinkedListNode(value, parent = self.end)
        if not self.root:
            self.root = newNode
        self.end = newNode
        self._count = self._count + 1


    def clear(self):
        """ Clearing removes all the items from the list """
        self.root = None
        self.end = None
        self._count = 0


    def removeLast(self):
        """
        Removes the last value in the list and returns its value
        
        @return: returns the last value from the list
        """
        if self.end == None:
            return None
        self._count = self._count - 1
        returnValue = self.end.value
        if self.end == self.root:
            self.end = self.root = None
        else:
            self.end = self.end.parent
            self.end.child = None
        return returnValue

    def values(self):
        """ Return a list containing all values in this linked list """
        list = []
        node = self.root
        while node:
            list.append(node.value)
            node = node.child
        return list


class LinkedListNode(object):
    """
    The nodes are bidirectional: each node has a reference to its parent and to
    its child. If the item is added to a non-empty list (child or parent given)
    the corresponding child or parent attribute is modified in the existing node
    (i.e. giving the node a child will make that child have the new node as its
    parent).
    """

    def __init__(self, value, parent=None, child=None):
        """ A default node has no parent or child, but a value must be given """
        self.value = value

        self.parent = parent
        if self.parent:
            self.parent.child = self

        self.child = child
        if self.child:
            self.child.parent = self
