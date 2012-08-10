# -*- coding: utf-8 -*-


__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:49:09$"

from Searcher import Searcher
import unittest

if __name__ == "__main__":
    print "This module contains units tests for module Searcher"

class  PySearcherTestCases(unittest.TestCase):
    def setUp(self):
        self.searcher = Searcher()

    def _testSomeTest(self):
       pass

def suite():
    return unittest.makeSuite(PySearcherTestCases,'test')

# Create unit tests