# -*- coding: utf-8 -*-
# Path hack.
import sys; import os; sys.path.insert(0, os.path.abspath('..'))

import unittest
# Import unit test of each module:
import SearcherUnitTest
import WordReaderUnitTest

#import os, sys, os.path;
#cwd = os.getcwd()
#print cwd
#support = os.path.join(cwd, '/../Support')
#print support
#
#sys.path.append(support), sys.path.append('../Trees')
#print sys.path


# Supporting modules
import Support.DataHandlingUnitTest as DataHandlingUnitTest
import Support.LinkedListUnitTest as LinkedListUnitTest
# Tree modules
import Trees.PartialTreeUnitTest as PartialTreeUnitTest
import Trees.RedBlackUnitTest as RedBlackUnitTest
import Trees.TrieUnitTest as TrieUnitTest
import Trees.TreeUnitTest as TreeUnitTest


if __name__ == '__main__':
    
    # Get all tests from each module unit test object
    suite = unittest.TestSuite((SearcherUnitTest.suite(),
                                TrieUnitTest.suite(),
                                WordReaderUnitTest.suite(),
                                RedBlackUnitTest.suite(),
                                LinkedListUnitTest.suite(),
                                TreeUnitTest.suite(),
                                DataHandlingUnitTest.suite(),
                                PartialTreeUnitTest.suite()))
    #    unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite)

