__author__="Patrik Ahvenainen"
__date__ ="$22.8.2012 14:52:54$"

# Path hack.
import sys; import os; sys.path.insert(0, os.path.abspath('..'))


from WordReader import WordReader
from Trees.Trie import Trie
from Trees.RedBlack import RedBlack
from Searcher import Searcher

import pickle

if __name__ == "__main__":
    print "Hello World";



    lukija = WordReader(["../Material/Grimm's Fairy Tales.txt"])
#    lukija.readWords()
    punamusta = RedBlack(lukija)
    trie = Trie(lukija)
#    print 'Adding all words to Punamusta'
#    punamusta.addFromReader()

    searcher = Searcher(trie, '')
    words = {}
    checklist = [0]*11
    while(True):
        word = searcher.randomWord()
        if len(word) > 10 or len(word) < 4:
            continue
        if not len(word) in words:
            words[len(word)] = [word]
        elif len(words[len(word)]) < 10:
            words[len(word)].append(word)
        else:
            words[len(word)].append(word)
            checklist[len(word)] = 1
        print word, checklist
        if sum(checklist[4:]) == 7:
            break

    pickle.dump( words, open( "save.p", "wb" ) )

    vals = pickle.load( open( "save.p", "rb" ) )
    print vals

