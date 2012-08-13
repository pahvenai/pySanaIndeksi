# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:52:12$"

from WordReader import WordReader
import unittest

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

linesIn2books = 8860 + 9571
noOfFiles = 2
wordsInTestFile = 50

class  PyWordReaderTestCases(unittest.TestCase):
    def setUp(self):
        self.lukija = WordReader(["../Material/Grimm's Fairy Tales.txt"],
                                 specialCharacters = ["-", "'"],
                                 acceptNumerals = True, acceptUpperCase = True,
                                 acceptLowerCase = False)
        # test addFileName
        self.lukija.addFileName("../Material/The Adventures of Tom Sawyer by Mark Twain.txt")

    def tearDown(self):
        self.lukija.clear('all')

    def testSanitize(self):
        """ Test whether word sanitizing works """
        self.words = []
        for word in unsanitizedWords:
            self.words.append(self.lukija.sanitize(word))
        self.assertEqual(self.words, sanitizedWords, 'Failed to sanitize words')

    def testCreateChrMap(self):
        """ Test whether index and character maps are okay """
        self.chrMap, self.idxMap = self.lukija._createChrMap()
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

    def testWordCountAndClear(self):
        """ Test if the reader finds the correct number of words """
        self.lukija = WordReader(['../Material/50words_in_UTF-8.txt'])
        self.lukija.readWords()
        self.assertEqual(self.lukija.wordcount , wordsInTestFile,
                             'Did not get the correct number of words')
        # After clearing, we should not have any words in memory
        self.lukija.clear()
        self.assertEqual((self.lukija.words, self.lukija.wordcount,
                          self.lukija.filecount, self.lukija.linecount),
                          ([], 0, 0, 0))


def suite():
    return unittest.makeSuite(PyWordReaderTestCases,'test')



if __name__ == "__main__":
    print "Running unit tests for WordReader module"
    runner = unittest.TextTestRunner()
    runner.run(suite())