# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 12:14:26$"

from WordReader import WordReader
from RedBlack import RedBlack
from Trie import Trie

import cProfile
import pstats

name = 'pySanaIndeksi'


def testRun():

    lukija = WordReader(["../Material/Grimm's Fairy Tales.txt"])
#                         "../Material/The Adventures of Tom Sawyer by Mark Twain.txt"])
#    lukija = WordReader(['../Material/50words_in_UTF-8.txt'])

    lukija.readWords()


    punamusta = RedBlack(lukija)
    trie = Trie(lukija)

    print "Adding words from selected material..."
    intti = 0; setti = 0
    for word in lukija.words:
        trie.add(word[0], word[1:])
        punamusta.add(word[0], word[1:])
        intti = intti + 1
        if intti > lukija.wordcount / 100.0:
            setti = setti + 1
            print setti, '% of words added'
            intti = 0

    print "Searching for words in Grimm's Fairy tales and The Adventures of Tom Sawyer"

    word = raw_input( "Find a word (or its beginning) in the text: " ).rstrip( '\n' )

    positions, count, linecount = trie.find(word)
    RBpositions, RBcount, RBlinecount = punamusta.find(word)
    print "Found", count, "instances (", linecount, "lines) @", positions
    print "Found", RBcount, "instances (", RBlinecount, "lines) @", RBpositions

if __name__ == "__main__":


    print '*' * 50, '\n', ' ' * ((50 - (len(name)))/2), name , '\n', '*' * 50
    cProfile.run('testRun()', 'testProf')
    p = pstats.Stats('testProf')
    p.sort_stats('cumulative').print_stats(10)


    #trie.printRandomRoute()

    #positions, count, linecount = trie.find('wor')
    #print "Found", count, "instances (", linecount, "lines) @", positions

#    print "Searching for words in Grimm's Fairy tales and The Adventures of Tom Sawyer"
#
#    word = raw_input( "Find a word (or its beginning) in the text: " ).rstrip( '\n' )
#
#    positions, count, linecount = trie.find(word)
#    RBpositions, RBcount, RBlinecount = punamusta.find(word)
#    print "Found", count, "instances (", linecount, "lines) @", positions
#    print "Found", RBcount, "instances (", RBlinecount, "lines) @", RBpositions
