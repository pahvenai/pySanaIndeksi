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

from sys import exit

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


operationOptions = {0: 'Exit', 1: 'Index file', 2: 'Choose indexer',
                    3: 'Unindex all files',  4: 'Do a search'}

trees = {0: {'RedBlack':RedBlack}, 1: {'Trie':Trie}}

def indexFile(tree, materialPath):
    """ Gives the user an option to choose which file to index to the tree """
    fileList = File.getFileNames(materialPath)
    printPath = File.printFileList(materialPath, noPath='yes')
    input = prompt('Choose file:', limits = [0, len(fileList)])
    print 'Indexing "' + printPath[input] + '" now...'
    tree.lukija.clear()
    tree.lukija.addFileName(fileList[input])
    tree.lukija.readWords()
    tree.addFromReader()

def unIndexAllFiles(tree):
    """ Removes all indexed words from the tree"""
    tree.clear()
    print 'Removed all words from index.'

def doSearch(tree):
    """ Searches the tree for the search phrase requested from the user """
    input = prompt('Give search phrase', type='str')
    if not input:
        print 'Cannot give an empty search phrase!'
        return
    searcher = Searcher(tree, input)
    print 'Searching...'
    searcher.search(printPretty=True)

def selectTree(tree):
    """ Gives the user the option to choose which tree to use """
    for index in trees:
        print index, trees[index].keys()[0] # prints: 0 RedBlack etc.
    input = prompt('Choose the tree:', [0, len(trees)-1])
    treeName = trees[input].keys()[0]
    print 'Indexer changed to ' + treeName +  ' and it is now empty'
    # retrieve a new tree from the chose input from the tree list
    tree = trees[input][treeName](tree.lukija)
    return tree

def printOperationOptions(status):
    """ Prints out the options for the user """
    print
    maxVal = 3 # number of operation that can be done to an empty index
    for index, key in enumerate(sorted(operationOptions)):
        if not (index >= maxVal and status == 'empty'):
            print key, '\t', operationOptions[key]

def operator(operation, tree, materialPath, status):
    """ Calls appropriate function according to the user's choice """
    if operation == 0:
        exit()
    elif operation == 1:
        indexFile(tree, materialPath)
        status = 'notEmpty'
    elif operation == 2:
        tree = selectTree(tree)
        status = 'empty'
    elif operation == 3:
        unIndexAllFiles(tree)
        status = 'empty'
    elif operation == 4:
        doSearch(tree)
    return tree, status

def printStarred(word):
    """ Prints the word and stars above and below it """
    print '*' * len(word), '\n', word, '\n', '*' * len(word)

def prompt(request = '', limits=[], type='int'):
    """ Asks the user for input, checks integer input for validity """
    if request: printStarred(request)
    print '>>',
    input = raw_input()
    # must be convertible to int
    if type == 'int':
        try:
            input = int(input)
            # if limits given value must be in the given range
            if limits:
                if input < limits[0] or input > limits[1]:
                    print 'Must give value between %d and %d' % (limits[0], limits[1])
                    input = prompt(request, limits=limits, type=type)
        except ValueError:
            print 'You must give an integer as an option here.'
            input = prompt(request, limits=limits, type=type)
    return input

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

    status = 'empty'
    while(input):
        printOperationOptions(status)
        input = prompt('Choose option (0 to quit):',
                       limits = [0, len(operationOptions)-1])
        tree, status = operator(input, tree, materialPath, status)





