# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:44:18$"

from LinkedList import LinkedList
import unittest

lastVal = 4
linkedListVals = [1, 2, 3, lastVal]
linkedListAfter = [1, 2, 3]

class PyLinkedListTestCases(unittest.TestCase):
    def setUp(self):
        self.list = LinkedList()

    def testLinkedList(self):
        """ Test adding multiple values to a linked list
            Tests, addLast(), values(), removeLast(), clear() and count
        """
        for val in linkedListVals:
            self.list.addLast(val)
        self.assertEqual(self.list.values() , linkedListVals,
                         'Linked list did not add values properly')
        self.assertEqual(self.list.removeLast() , lastVal,
                         'Linked list did not return correct last value')
        self.assertEqual(self.list.values(), linkedListAfter,
                         'Linked list removing did not work')
        self.list.clear()
        self.assertFalse(self.list.values(), 'Linked list did not clear')
        self.assertFalse(self.list.count(), 'Linked list did not clear')

def suite():
    return unittest.makeSuite(PyLinkedListTestCases,'test')


if __name__ == "__main__":
    print "Running unit tests for LinkedList module"
    runner = unittest.TextTestRunner()
    runner.run(suite())