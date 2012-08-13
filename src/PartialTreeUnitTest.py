# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$13.8.2012 14:52:35$"

from PartialTree import PartialTree
import unittest


class  PyPartialTreeTestCases(unittest.TestCase):

    def testCannotBeInstantiated(self):
        """ This abstract class should not be possible to instantiate """
        self.assertRaises(TypeError, PartialTree)

def suite():
    return unittest.makeSuite(PyPartialTreeTestCases,'test')


if __name__ == "__main__":
    print "Running unit tests for PartialTree module"
    runner = unittest.TextTestRunner()
    runner.run(suite())