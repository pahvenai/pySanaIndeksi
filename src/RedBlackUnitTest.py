# -*- coding: utf-8 -*-


__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:47:25$"

from RedBlack import RedBlack
from WordReader import WordReader
import unittest

if __name__ == "__main__":
    print "This module contains unit tests for module RedBlack"

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
        self.lukija.addFileNames(["../Material/50words_in_UTF-8.txt"])
        self.redblack = RedBlack(self.lukija)

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
        for object in MultiWordAdd:
            self.redblack.add(object[0], object[1:]) # Add words to Trie

        pos, _, _ = self.redblack.find('a')
        self.assertEqual(pos, MultiWordFindA,
                         'RB: Error finding multiple instances of a word')
        pos, _, _ = self.redblack.find('b')
        self.assertEqual(pos, MultiWordFindB,
                         'RB: Error finding multiple instances of a word')

def suite():
    return unittest.makeSuite(PyRedBlackTestCases,'test')