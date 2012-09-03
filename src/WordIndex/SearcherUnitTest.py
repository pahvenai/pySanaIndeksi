# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:49:09$"

# Path hack.
import sys; import os; sys.path.insert(0, os.path.abspath('..'))

from Searcher import Searcher
from Trees.Trie import Trie
from WordReader import WordReader
import unittest

MaterialFilePath = "../../Material/Grimm's Fairy Tales.txt"

operations = {"Basic": "brothers", "partial": "Grimm*",
              "NOT": "grimm* NOT brothers", "OR": "Grimm* OR brothers",
              "AND": "grimm* AND brothers", "XOR": "grimm XOR brothers"}

binaryOperationsSearch = {"Grimm*": 10, "brothers": 40, "grimm* NOT brothers": 4,
                          "Grimm* OR brothers": 44, "grimm* XOR brothers": 38,
                          "grimm* AND brothers": 6,
                          "fierce XOR rock": 8,
                           "milk AND cow": 4}

class  PySearcherTestCases(unittest.TestCase):
    def setUp(self):
        self.reader = WordReader()
        self.finder = Trie(self.reader)
        self.searcher = Searcher(self.finder, '')

    def tearDown(self):
        self.reader = None
        self.finder = None
        self.searcher = None

    def testRandomWord(self):
       """ Tests that non-empty words are found and they are not the same """
       word1 = self.searcher.randomWord()
       word2 = self.searcher.randomWord()
       self.assertTrue(len(word1) > 1, 'Word length too short')
       self.assertTrue(len(word2) > 1, 'Word length too short')
       self.assertNotEqual(word1, word2, 'Found the same word')

    def testRandomWords(self):
       """ Tests that a set of random words do not contain the same words """
       words = self.searcher.randomWord(5)
       self.assertTrue(len(set(words)) == 5, 'Did not find 5 unique words')

    def testBinaryOperationsAreWorking(self):
        """
        Checks that operations are not identic and that correct number of hits
        is returned for every known result.
        """
        self.reader.addFileName(MaterialFilePath, readNow=True)
        self.finder.addFromReader()

        results = []
        for operation in operations:
            results.append(self.searcher.search(operations[operation],
                                                returnCount=True))
        self.assertTrue(len(set(results)) == 6, #i.e. operations are not identic
                        'Searcher failed binary operation check')
        for searchTerm in binaryOperationsSearch:
            self.assertEqual(self.searcher.search(searchTerm, returnCount=True),
                             binaryOperationsSearch[searchTerm],
                            'Searcher found wrong number of hits on some search')

def suite():
    return unittest.makeSuite(PySearcherTestCases,'test')


if __name__ == "__main__":
    print "Running unit tests for Searcher module"
    runner = unittest.TextTestRunner()
    runner.run(suite())