# -*- coding: utf-8 -*-

import unittest
from WordReader import WordReader
from RedBlack import RedBlack
from Trie import Trie

# Note: the test cases are written for a version of the WordReader that accepts
# only alphanumerals, hyphens and apostrophes. The code itself allows one to
# easily change the accepted characters.

unsanitizedWords = ["32'verregö ", 'dseFR-fw- ert', '  dfg', '¤gf', '4egdFB']
sanitizedWords =   ["32'VERREG"  , 'DSEFR-FW-'    , 'DFG'  , ''   , '4EGDFB']

properChrMap = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '-',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                "'"]

properIdxMap = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
                '-':10,
                'A':11, 'B':12, 'C':13, 'D':14, 'E':15, 'F':16, 'G':17, 'H':18,
                'I':19, 'J':20, 'K':21, 'L':22, 'M':23, 'N':24, 'O':25, 'P':26,
                'Q':27, 'R':28, 'S':29, 'T':30, 'U':31, 'V':32, 'W':33, 'X':34,
                'Y':35, 'Z':36,
                "'": 37}

linesIn2books = 8859 + 9571
noOfFiles = 2
wordsInTestFile = 50

WordsToAdd = [('ww3fwG', 99, 1), ('Sana', 3, 2), ('ed', 2222, 1),
              ('Tampere', 1003, 1), ('Rekka-auto', 2, 1), ("Don't", 22, 2)]

class  PyWordReaderTestCases(unittest.TestCase):
    def setUp(self):
        self.lukija = WordReader(["../Material/Grimm's Fairy Tales.txt",
                         "../Material/The Adventures of Tom Sawyer by Mark Twain.txt"])
    #    self.foo = PyUnit()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    

    def testSanitize(self):
        """ Test whether word sanitizing works """
        self.words = []
        for word in unsanitizedWords:
            self.words.append(self.lukija.sanitize(word))
        self.assertEqual(self.words, sanitizedWords, 'Failed to sanitize words')

    def testCreateChrMap(self):
        """ Test whether index and character maps are okay """
        self.chrMap, self.idxMap = self.lukija.createChrMap()
        self.assertEqual(self.chrMap, properChrMap, 'Bad character map')
        self.assertEqual(self.idxMap, properIdxMap, 'Bad index map')

    def testInd2char(self):
        """ Test function ind2char """
        for index, val in enumerate(properChrMap):
            self.assertEqual(self.lukija.ind2char(index), properChrMap[index],
                             'ind2char function failed to map indices to characters')

    def testChar2ind(self):
        """ Test function ind2char """
        for char in properIdxMap:
            self.assertEqual(self.lukija.char2ind(char), properIdxMap[char],
                             'char2ind function failed to map characters to indices')

    def testGetCharMapSize(self):
        """ Test whether getCharMapSize returns the correct value """
        self.assertEqual(self.lukija.getCharMapSize(), len(properChrMap),
                             'getCharMapSize returned wrong map size')

    def testLineCount(self):
        """ Test whether WordReader reads all lines in files """
        self.lukija.readWords()
        self.assertEqual(self.lukija.linecount , linesIn2books,
                             'Did not read correct number of lines from file')
        self.assertEqual(self.lukija.filecount , noOfFiles,
                             'Did not read correct number of lines from file')

    def testWordCount(self):
        """ Test if the reader finds the correct number of words """
        self.lukija = WordReader(['../Material/50words_in_UTF-8.txt'])
        self.lukija.readWords()
        self.assertEqual(self.lukija.wordcount , wordsInTestFile,
                             'Did not get the correct number of words')


class  PyTrieTestCases(unittest.TestCase):
    def setUp(self):
        self.lukija = WordReader(["../Material/Grimm's Fairy Tales.txt",
                         "../Material/The Adventures of Tom Sawyer by Mark Twain.txt"])
        self.trie = Trie(self.lukija)
        
    def testSimpleAddFind(self):
        """ Add some objects to Trie and see if you can find them """
        checklist = []
        for word in WordsToAdd:
            self.trie.add(word) # Add words to Trie
        for word in WordsToAdd:
            # Get the position of each word
            pos, _, _ = self.trie.find(word[0],'exact')
            # We add the word and the found positions to match list formatting
            # to the input
            checklist.append((word[0], pos[0][0], pos[0][1]))
        self.assertEqual(checklist , WordsToAdd,
                         'Did not find all words that were supposed to add')        
        

if __name__ == '__main__':
    unittest.main()

