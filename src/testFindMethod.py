__author__="Patrik Ahvenainen"
__date__ ="$22.8.2012 14:52:54$"

from WordReader import WordReader
from Trie import Trie
from RedBlack import RedBlack
from Searcher import Searcher

import cProfile
import pstats
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

#    print 'Adding all words to Trie'
##    trie.addFromReader()
#    cProfile.run("trie.addFromReader()", 'testProf')
#    p = pstats.Stats('testProf')
#    p.sort_stats('cumulative').print_stats(25)
#
#    cProfile.run("for i in range(100000): trie.find('SANA', sanitized=True)", 'testProf')
#    p = pstats.Stats('testProf')
#    p.sort_stats('cumulative').print_stats(25)