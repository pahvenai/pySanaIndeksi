# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Patrik Ahvenainen"
__date__ ="$6.8.2012 13:26:52$"

if __name__ == "__main__":
    print "This module contains a simple linked list class"


class LinkedList:
    def __init__(self):
        self.root = None
        self.end = None
        self.count = 0

    def addLast(self, value):
        """ Add one value to the end of the list """
        newNode = LinkedListNode(value, parent = self.end)
        if not self.root:
            self.root = newNode
        self.end = newNode
        self.count = self.count + 1

    def values(self):
        """ Return a list containing all value in this linked list """
        list = []
        node = self.root
        while node:
            list.append(node.value)
            node = node.child
        return list

class LinkedListNode:

    def __init__(self, value, parent=None, child=None):
        self.value = value
        self.parent = parent
        if self.parent:
            self.parent.child = self
        self.child = child
