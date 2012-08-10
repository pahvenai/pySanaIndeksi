# -*- coding: utf-8 -*-


__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:50:51$"

from Trie import Trie
from WordReader import WordReader
import unittest

if __name__ == "__main__":
    print "This module contains units tests for module Trie"

WordsToAdd = [('ww3fwG', 99, 1), ('Sana', 3, 2), ('ed', 2222, 1),
              ('Tampere', 1003, 1), ('Rekka-auto', 2, 1), ("Don't", 22, 2)]

MultiWordAdd = [('c', 20, 3), ('a', 1, 1), ('c', 23, 1), ('b', 2, 1), ('a', 3, 1),
                ('a', 1 ,2 ), ('b', 2, 2), ('a', 3, 2), ('ade', 2, 3)]
MultiWordFindA = [(1,1), (3,1), (1,2), (3,2)]
MultiWordFindB = [(2,1), (2,2)]


class  PyTrieTestCases(unittest.TestCase):
    def setUp(self):
        self.lukija = WordReader()
        # test addFileNames
        self.lukija.addFileNames(["../Material/The Adventures of Tom Sawyer by Mark Twain.txt"])
        self.trie = Trie(self.lukija)

    def testSimpleAddFind(self):
        """ Add some objects to Trie and see if you can find them """
        checklist = []
        for object in WordsToAdd:
            self.trie.add(object[0], object[1:]) # Add words to Trie
        for word in WordsToAdd:
            # Get the position of each word
            pos, _, _ = self.trie.find(word[0],'exact')
            # We add the word and the found positions to match list formatting
            # to the input
            checklist.append((word[0], pos[0][0], pos[0][1]))
        self.assertEqual(checklist , WordsToAdd,
                         'Trie: Did not find all words that were supposed to add')

    def testMultiWordFind(self):
        for object in MultiWordAdd:
            self.trie.add(object[0], object[1:]) # Add words to Trie
        pos, _, _ = self.trie.find('a','exact')
        self.assertEqual(pos, MultiWordFindA,
                         'Trie: Error finding multiple instances of a word')
        pos, _, _ = self.trie.find('b','exact')
        self.assertEqual(pos, MultiWordFindB,
                         'Trie: Error finding multiple instances of a word')

                       
def suite():
    return unittest.makeSuite(PyTrieTestCases,'test')