# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:55:42$"

import DataHandling
import unittest

class  PyDataHandlingTestCases(unittest.TestCase):
    def setUp(self):
        pass


    def _testSomeTest(self):
       pass

def suite():
    return unittest.makeSuite(PyDataHandlingTestCases,'test')


# Create unit tests

if __name__ == "__main__":
    print "Running unit tests for DataHandling module"
    runner = unittest.TextTestRunner()
    runner.run(suite())