# -*- coding: utf-8 -*-

import unittest
# Import unit test of each module:
import WordReaderUnitTest
import TrieUnitTest
import SearcherUnitTest
import RedBlackUnitTest
import LinkedListUnitTest
import PuuUnitTest
import DataHandlingUnitTest


if __name__ == '__main__':
    # Get all tests from each module unit test object
    suite = unittest.TestSuite((WordReaderUnitTest.suite(),
                                TrieUnitTest.suite(),
                                SearcherUnitTest.suite(),
                                RedBlackUnitTest.suite(),
                                LinkedListUnitTest.suite(),
                                PuuUnitTest.suite(),
                                DataHandlingUnitTest.suite()))
    #    unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite)

