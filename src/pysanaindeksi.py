# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 12:14:26$"

from WordReader import WordReader
from RedBlack import RedBlack
from Trie import Trie
import DataHandling as File
from Searcher import Searcher

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
    print "Found", count, "instances (", linecount, "lines) @", positions
    RBpositions, RBcount, RBlinecount = punamusta.find(word)
    print "Found", RBcount, "instances (", RBlinecount, "lines) @", RBpositions


operationOptions = {'0': 'Exit', '1': 'Index file',
                    '2': 'Unindex all files',  '3': 'Do a search',
                    '4': 'Choose indexer'}

def indexFile(tree, materialPath):
    print 'Choose file'
    fileList = File.getFileNames(materialPath)
    File.printFileList(materialPath)
    input = raw_input()
    try:
        if int(input) >= len(fileList) or  int(input) < 0:
            print '"' + input +'"' + ' is a bad file name option'
            return
    except ValueError:
        print 'You must give an integer as an option here.'
        return
    path = fileList[int(input)]
    print 'Indexing "' + path + '" now...'
    tree.lukija.clear()
    tree.lukija.addFileName(path)
    tree.lukija.readWords()
    tree.addFromReader()

def unIndexAllFiles(tree):
    tree.clear()
    print 'Removed all words from index.'

def doSearch(tree):
    print 'Give search phrase'
    input = raw_input()
    if not input:
        print 'Cannot give an empty search phrase-'
        return
    searcher = Searcher(tree, input)
    print 'Searching...'
    values = searcher.search(printPretty=True)

def printOperationOptions():
    for key in sorted(operationOptions):
        print key, '\t', operationOptions[key]

def operator(operation, tree, materialPath):
    if operation == '1':
        indexFile(tree, materialPath)
    if operation == '2':
        unIndexAllFiles(tree)
    if operation == '3':
        doSearch(tree)

if __name__ == "__main__":

    lukija = WordReader()
    tree = Trie(lukija)
    materialPath = '../Material/'
    if not File.getFileNames:
        raise Exception('Empty file path, cannot find material')

    print '*' * 50, '\n', ' ' * ((50 - (len(name)))/2-1), name , '\n', '*' * 50

#    cProfile.run('testRun()', 'testProf')
#    p = pstats.Stats('testProf')
#    p.sort_stats('cumulative').print_stats(10)


    #File.printFileList('../Material/')

    input = '0'
    while(input):
        print 'Choose option (Press Enter to quit):'
        printOperationOptions()
        input = raw_input()
        operator(input, tree, materialPath)
        if not input or input == '0':
            break



