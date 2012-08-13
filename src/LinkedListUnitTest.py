# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:44:18$"

from LinkedList import LinkedList
import unittest

linkedListVals = [1, 2, 3, 4]

class PyLinkedListTestCases(unittest.TestCase):
    def setUp(self):
        self.list = LinkedList()

    def testAddition(self):
        """ Test adding multiple values to a linked list """
        for val in linkedListVals:
            self.list.addLast(val)
        self.assertEqual(self.list.values() , linkedListVals,
                         'Linked list did not add values properly')

def suite():
    return unittest.makeSuite(PyLinkedListTestCases,'test')


if __name__ == "__main__":
    print "Running unit tests for LinkedList module"
    runner = unittest.TextTestRunner()
    runner.run(suite())