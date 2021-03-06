# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:47:25$"

# Path hack.
import sys; import os; sys.path.insert(0, os.path.abspath('..'))

from RedBlack import RedBlack
from WordIndex.WordReader import WordReader
import unittest

WordsToAdd = [('ww3fwG', 99, 1), ('Sana', 3, 2), ('ed', 2222, 1),
              ('Tampere', 1003, 1), ('Rekka-auto', 2, 1), ("Don't", 22, 2)]

MultiWordAdd = [('c', 20, 3), ('a', 1, 1), ('c', 23, 1), ('b', 2, 1), ('a', 3, 1),
                ('a', 1 ,2 ), ('b', 2, 2), ('a', 3, 2), ('ade', 2, 3)]
MultiWordFindA = [(1,1), (3,1), (1,2), (3,2)]
MultiWordFindB = [(2,1), (2,2)]


class  PyRedBlackTestCases(unittest.TestCase):
    def setUp(self):
        self.lukija = WordReader()
        # test addFileNames
        self.redblack = RedBlack(self.lukija)

    def tearDown(self):
        self.lukija.clear('all')
        self.redblack.clear()
        self.lukija = None
        self.redblack = None

    def testSimpleAddFind(self): # Red Black would fail this test now
        """ Add some objects to Red Black tree and see if you can find them """
        checklist = []
        for object in WordsToAdd:
            self.redblack.add(object[0], object[1:]) # Add words to Trie
        for word in WordsToAdd:
            # Get the position of each word
            pos, _,  _ = self.redblack.find(word[0])
            # We add the word and the found positions to match list formatting
            # to the input
            checklist.append((word[0], pos[0][0], pos[0][1]))
        self.assertEqual(checklist , WordsToAdd,
                         'Did not find all words that were supposed to add')

        self.redblack.clear()
        self.lukija.readWords()
        self.redblack.addFromReader()



    def testMultiWordFind(self):
        """ Tests that multiple instances of a word are found correctly """
        for object in MultiWordAdd:
            self.redblack.add(object[0], object[1:]) # Add words to Trie

        pos, _, _ = self.redblack.find('a')
        self.assertEqual(pos, MultiWordFindA,
                         'RB: Error finding multiple instances of a word')
        pos, _, _ = self.redblack.find('b')
        self.assertEqual(pos, MultiWordFindB,
                         'RB: Error finding multiple instances of a word')

    def testWordCounter(self):
        """ Tests that both the reader and the tree can count the words """
        self.lukija.clear('all')
        self.lukija.addFileNames(["../../Material/50words_in_UTF-8.txt"])
        self.assertEqual(self.lukija.wordcount, 0,
                         'RB: WordReader clearing failed')
        self.lukija.readWords()
        self.assertEqual(self.lukija.wordcount, 50,
                         'RB: WordReader failed in reading words')
        self.redblack.clear()
        self.redblack.addFromReader()
        self.assertEqual(self.redblack.wordCount, 50,
                         'RB: word counting failed')

def suite():
    return unittest.makeSuite(PyRedBlackTestCases,'test')



if __name__ == "__main__":
    print "Running unit tests for RedBlack module"
    runner = unittest.TextTestRunner()
    runner.run(suite())