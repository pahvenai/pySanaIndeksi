# -*- coding: utf-8 -*-

import unittest
# Import unit test of each module:
import DataHandlingUnitTest
import LinkedListUnitTest
import PartialTreeUnitTest
import RedBlackUnitTest
import SearcherUnitTest
import TrieUnitTest
import TreeUnitTest
import WordReaderUnitTest

if __name__ == '__main__':
    # Get all tests from each module unit test object
    suite = unittest.TestSuite((WordReaderUnitTest.suite(),
                                TrieUnitTest.suite(),
                                SearcherUnitTest.suite(),
                                RedBlackUnitTest.suite(),
                                LinkedListUnitTest.suite(),
                                TreeUnitTest.suite(),
                                DataHandlingUnitTest.suite(),
                                PartialTreeUnitTest.suite()))
    #    unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite)

