# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:46:28$"

from Tree import Tree
import unittest


class  PyTreeTestCases(unittest.TestCase):

    def testCannotBeInstantiated(self):
        """ This abstract class should not be possible to instantiate """
        self.assertRaises(TypeError, Tree)

def suite():
    return unittest.makeSuite(PyTreeTestCases,'test')



if __name__ == "__main__":
    print "Running unit tests for Tree module"
    runner = unittest.TextTestRunner()
    runner.run(suite())

