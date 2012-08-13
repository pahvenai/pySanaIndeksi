# -*- coding: utf-8 -*-


__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:46:28$"

from Tree import Tree
import unittest

if __name__ == "__main__":
    print "Contains unit tests for Puu abstract class"

class  PyTreeTestCases(unittest.TestCase):
    def setUp(self):
        self.tree = Tree()

    def _testSomeTest(self):
       pass

def suite():
    return unittest.makeSuite(PyTreeTestCases,'test')

# Create unit tests

