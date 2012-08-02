__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 12:14:26$"

from WordReader import WordReader
from RedBlack import RedBlack
from Trie import Trie

name = 'pySanaIndeksi'

if __name__ == "__main__":
    print '*' * 50, '\n', ' ' * ((50 - (len(name)))/2), name , '\n', '*' * 50

    lukija = WordReader(["../Material/Grimm's Fairy Tales.txt",
                         "../Material/The Adventures of Tom Sawyer by Mark Twain.txt"])

    lukija.readWords()


    punamusta = RedBlack(lukija)
    trie = Trie(lukija)

    for word in lukija.words:
        trie.add(word)

    trie.printRandomRoute()

    #positions, count, linecount = trie.find('wor')
    #print "Found", count, "instances (", linecount, "lines) @", positions

    print "Searching for words in Grimm's Fairy tales and The Adventures of Tom Sawyer"

    word = raw_input( "Find a word (or its beginning) in the text: " ).rstrip( '\n' )

    positions, count, linecount = trie.find(word)
    print "Found", count, "instances (", linecount, "lines) @", positions
