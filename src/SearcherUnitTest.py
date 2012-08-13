# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:49:09$"

from Searcher import Searcher
from RedBlack import RedBlack
import unittest


class  PySearcherTestCases(unittest.TestCase):
    def setUp(self):
        self.finder = RedBlack()
        self.searcher = Searcher(self.finder, '')

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




def suite():
    return unittest.makeSuite(PySearcherTestCases,'test')

# Create unit tests



if __name__ == "__main__":
    print "Running unit tests for Searcher module"
    runner = unittest.TextTestRunner()
    runner.run(suite())