# -*- coding: utf-8 -*-


__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:55:42$"

import DataHandling
import unittest

if __name__ == "__main__":
    print "Module contains unit tests for DataHandling module"

class  PyDataHandlingTestCases(unittest.TestCase):
    def setUp(self):
        pass


    def _testSomeTest(self):
       pass

def suite():
    return unittest.makeSuite(PyDataHandlingTestCases,'test')


# Create unit tests
