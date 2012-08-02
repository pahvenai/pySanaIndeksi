# -*- coding: utf-8 -*-

import unittest
from WordReader import WordReader, sanitize
from RedBlack import RedBlack
from Trie import Trie

unsanitizedWords = ['32verregö ', 'dseFRfw ert', '  dfg', '¤gf', '4egdFB']
sanitizedWords =   ['32VERREG'  , 'DSEFRFW'    , 'DFG'  , ''   , '4EGDFB']


class  PyUnitTestCase(unittest.TestCase):
    #def setUp(self):
    #    self.lukija = WordReader("../Material/Grimm's Fairy Tales.txt")
    #    self.foo = PyUnit()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    

    def testSanitize(self):
        """ Test whether word sanitizing works """
        testWords = []
        for word in unsanitizedWords:
            testWords.append(sanitize(word))
        print testWords
        print sanitizedWords
        self.assertEqual(testWords, sanitizedWords, 'Failed to sanitize words')

if __name__ == '__main__':
    unittest.main()

