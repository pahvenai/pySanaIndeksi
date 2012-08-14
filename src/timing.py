# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$14.8.2012 12:02:36$"

#

from time import time
from WordReader import WordReader
from RedBlack import RedBlack
from Trie import Trie

def timeThis(func):
    def wrapper(*arg):
        t1 = time()
        res = func(*arg)
        t2 = time()
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


def addWordsToEmptyList(tree, words, repeats, string):

    @timeThis
    def boo(tree, words):
        tree.addFromReader(words)

    runtimes = []
    for i in range(0, repeats):
        tree.clear()
        runtimes.append( boo(tree, words) )
    print string + '%8.3f ms \t %6.3f ms' %  (average(runtimes), average(runtimes)/words)

def findWords(tree, word, repeats, string):

    @timeThis
    def boo(tree, word, repeatcount):
        for i in range(0, repeatcount):
            tree.find(word)

    runtimes = []
    for i in range(0, repeats):
        runtimes.append( boo(tree, word, 1000) )
    print string + '%8.3f ms' %  (sum(runtimes) / repeats)


if __name__ == "__main__":
    print "Hello World"

    lukija = WordReader(["../Material/Grimm's Fairy Tales.txt"])
    lukija.readWords()
    punamusta = RedBlack(lukija)
    trie = Trie(lukija)

    repeats = 10;
#    for i in range(2,17):
#        addWordsToEmptyList(trie, 2**i, repeats, '%15s\t%10d\t' % ('trie', 2**i))
#    for i in range(2,17):
#        addWordsToEmptyList(punamusta, 2**i, repeats, '%15s\t%10d\t' % ('punamusta', 2**i))
    punamusta.addFromReader()
    trie.addFromReader()
    for i in range(1,20):
        findWords(trie, 'a'*i, repeats, '%15s\t%25s\t' % ('trie', 'a'*i))
    for i in range(1,20):
        findWords(punamusta, 'a'*i, repeats, '%15s\t%25s\t' % ('punamusta', 'a'*i))

    

