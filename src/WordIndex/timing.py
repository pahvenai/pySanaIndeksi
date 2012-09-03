import random
# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$14.8.2012 12:02:36$"

# Path hack.
import sys; import os; sys.path.insert(0, os.path.abspath('..'))


import time
from WordReader import WordReader
from Trees.RedBlack import RedBlack
from Trees.Trie import Trie
from Support.DataHandling import openFile
import pickle

def timeThis(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        runtime = ((t2-t1)*1000.0)
        return runtime
    return wrapper

def average(values):
    return sum(values) / len(values)

def repeat(repeats):
    def wrap(f):
        def wrapped_f(*args):
            runtimes = []
            for i in range(0, repeats):
                runtimes.append(f(*args))
            return runtimes
        return wrapped_f
    return wrap


def addWordsToEmptyList(tree, words, repeats, string, printout=True):

    @timeThis
    def boo(tree, words):
        tree.addFromReader(words)

    runtimes = []
    for i in range(0, repeats):
        tree.clear()
        runtimes.append( boo(tree, words) )
        time.sleep(0.01)
    if printout:
        print string + '%8.3f ms %8.3f ms' %  (average(runtimes), average(runtimes)/words)
    else:
        return average(runtimes)

def findWords(tree, words, repeats, string='', printout=True):

    @timeThis
    def boo(tree, word, repeatcount):
        for i in range(0, repeatcount):
            tree.find(word, sanitized=True, output='boolean')

    runtimes = []
    for i in range(0, repeats):
        word = random.choice(words)
        word = tree.lukija.sanitize(word)
        runtimes.append( boo(tree, word, 1000) )
        time.sleep(0.01)
    if not printout:
        return average(runtimes)
    else:
        print string + '%20.3f ms' %  (sum(runtimes) / repeats)


if __name__ == "__main__":
    print "Hello World"

    trieAddFile = openFile('trieAddToEmpty', 'w')
    punamustaAddFile = openFile('punamustaAddToEmpty', 'w')
    trieFindLengthFile = openFile('trieFindWordLength', 'w')
    punamustaFindLengthFile = openFile('punamustaFindWordLength', 'w')
    trieFindWordCountFile = openFile('trieFindWordCount', 'w')
    punamustaFindWordCountFile = openFile('punamustaFindWordCoun', 'w')

    lukija = WordReader(["../Material/Grimm's Fairy Tales.txt"])
    lukija.readWords()
    punamusta = RedBlack(lukija)
    trie = Trie(lukija)

    words = pickle.load( open( "randomWordList", "rb" ) ) # indexed by word len

    repeats = 100;
    runtimes = []
    for i in range(2,17):
        runtime = addWordsToEmptyList(trie, 2**i, repeats, '%25s\t%10d\t' % ('trie:add', 2**i), False)
        print '%25s\t%10d\t\t%14.3f ms' % ('trie:addToEmpty', 2**i, runtime)
        trieAddFile.write('%10d\t%8.3f\n' % (2**i, runtime))
        runtimes.append(findWords(trie, words[7], repeats, printout=False))
    for index, runtime in enumerate(runtimes):
        print '%25s\t%10d\t\t%14.3f ms' % ('trie:findWordCount', 2**(index+2), runtime)
        trieFindWordCountFile.write('%10d\t%14.3f\n' % (2**(index+2), runtime))

    runtimes = []
    for i in range(2,17):
        runtime = addWordsToEmptyList(punamusta, 2**i, repeats, '%25s\t%10d\t' % ('punamusta:addToEmpty', 2**i), False)
        print '%25s\t%10d\t\t%14.3f ms' % ('punamusta:addToEmpty', 2**i, runtime)
        punamustaAddFile.write('%10d\t%8.3f\n' % (2**i, runtime))
        runtimes.append(findWords(punamusta, words[7], repeats, printout=False))
    for index, runtime in enumerate(runtimes):
        print '%25s\t%10d\t%8.3f ms' % ('punamusta:findWordCount', 2**(index+2), runtime)
        punamustaFindWordCountFile.write('%10d\t%14.3f\n' % (2**(index+2), runtime))

    print 'Adding all words to Punamusta'
    punamusta.addFromReader()
    print 'Adding all words to Trie'
    trie.addFromReader()


    for i in range(4,10+1):
        runtime = findWords(trie, words[i], repeats, printout=False)
        print '%25s\t%10d\t\t%14.3f ms' % ('trie:findWordLength', i, runtime)
        trieFindLengthFile.write('%10d\t%14.3f\n' % (i, runtime))
    for i in range(4,10+1):
        runtime = findWords(punamusta, words[i], repeats, printout=False)
        print '%25s\t%10d\t\t%14.3f ms' % ('punamusta:findWordLength', i, runtime)
        punamustaFindLengthFile.write('%10d\t%14.3f\n' % (i, runtime))

    

