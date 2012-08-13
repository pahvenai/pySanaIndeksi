# -*- coding: utf-8 -*-


__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:46:28$"

from Puu import Puu
import unittest

if __name__ == "__main__":
    print "Contains unit tests for Puu abstract class"

class  PyPuuTestCases(unittest.TestCase):
    def setUp(self):
        self.puu = Puu()

    def _testSomeTest(self):
       pass

def suite():
    return unittest.makeSuite(PyPuuTestCases,'test')

# Create unit tests

