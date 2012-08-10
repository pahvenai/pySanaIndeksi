# -*- coding: utf-8 -*-

__author__="Patrik Ahvenainen"
__date__ ="$8.8.2012 12:32:57$"


from RedBlack import RedBlack
from WordReader import WordReader
from LinkedList import LinkedList


class Searcher(object):
    '''
    This class provides a simple set-based searching methods. Searches comprise
    of set operations between individual find-operations for each given word.

    The individual word searches are done with the input object finder using its
    find method for each word. Before word searches, the individual words are
    sanitized with sanitizer or finder's sanitizer using the sanitize method.

    The search supports keywords AND, NOT, OR and XOR corresponding to set
    operations intersection, difference, union and symmetric difference.

    Basic operation:
    searcher = Searcher(finderObject, "word1 AND word2") # initialize
    results = searcher.search() # Get the hits from the word search

    methods:
    self.search():                  Completes the search and returns the hits

    internal functions:
    self._checkString():            Checks that the seach phrase is good
    self._recursiveSearch(index):   Starting from given index goes through the
                                    search string until it finds a closing
                                    paranthesis or runs out of search string
    self._setOperate(left, right, operation):
                                    Does the given set operation to the two sets
    '''



    def __init__(self, finder, searchString, sanitizer=None):
        self.str = searchString
        self.finder = finder
        self.sanitizer = sanitizer
        if not sanitizer:
            self.sanitizer = self.finder.lukija
        self.words = searchString.split()
        self.operations = ['AND', 'OR', 'NOT', 'XOR']
        self.paranthesis = ['(', ')']
        self.status = 'ok'
        self._checkString() #may flag status as bad
        self.set = set()

    def search(self, searchPhrase=None):
        """ Search the given search phrase using recursive search """
        if searchPhrase:
            self.words = searchPhrase.split()
            self._checkString()
        if not self.status == 'ok':
            return None
        return self._recursiveSearch(0)


    def _checkString(self):
        self.types = []
        for word in self.words:
            if word in self.operations:
                self.types.append('O')
            elif word in self.paranthesis:
                self.types.append(word)
            else:
                self.types.append('W')

        itemCount = len(self.types)
        paranthesisList = LinkedList()
        self.pList = [0] * len(self.types)
        pVal = 0
        for index, word in enumerate(self.words):
            if self.types[index] == 'W':
                # Words cannot be empty
                if self.sanitizer.sanitize(word) == '':
                    self.status = 'bad'
                    return
            if self.types[index] == '(':
                paranthesisList.addLast('(')
                pVal = pVal + 1
                self.pList[index] = pVal
            if self.types[index] == ')':
                self.pList[index] = pVal
                pVal = pVal - 1
                if paranthesisList.values():
                    paranthesisList.removeLast()
                else:
                    self.status = 'bad'
                    return
            if self.types[index] == 'O':
                if index > 0:
                    if not self.types[index-1] == 'O':
                        pass
                else:
                    self.status = 'bad'
                    return
                if index < itemCount - 1:
                    if not self.types[index+1] == 'O':
                        pass
                else:
                    self.status = 'bad'
                    return
        if paranthesisList.values():
            self.status = 'bad'
            return

    def _recursiveSearch(self, index):
        pSkip = 0 # parenthesis skip: this word is handled elsewhere
        left = None
        right = None
        for index in range(index, len(self.types)):
            # skip words that are inside parenthesis
            if pSkip:
                if self.pList[index] == pSkip:
                    pSkip = 0
                    continue
                else:
                    continue

            # At the end of parenthesis return the set and return to caller
            if self.types[index] == ')':
                return left

            # When parenthesis start, make a recursive call that covers the
            # set inside the parenthesis
            if self.types[index] == '(':
                pSkip = self.pList[index]
                if left == None:
                    left = self._recursiveSearch(index + 1)
                else:
                    right = self._recursiveSearch(index + 1)

            # Find the word and return its positions as a set
            if self.types[index] == 'W':
                if left == None:
                    left = set(self.finder.find(self.words[index], output='list'))
                else:
                    right = set(self.finder.find(self.words[index], output='list'))

            # Set the operator tag to the desired operation
            if self.types[index] == 'O':
                operator = self.words[index]
            else:
                # If two sides of the operation exist, operate on them
                if (not left==None) and (not right == None):
                    left = self._setOperate(left, right, operator)
                    right = None

        return left # return the positions searched for

    def _setOperate(self, left, right, operator):
        """ Returns the set from the set operation of two sets """
        if operator == 'AND':
            left = left & right
        elif operator == 'OR':
            left = left | right
        elif operator == 'XOR':
            left = left ^ right
        elif operator == 'NOT':
            left = left - right
        return left

if __name__ == "__main__":
    inputFiles = ["../Material/Grimm's Fairy Tales.txt"]
    lukija = WordReader(inputFiles)
    finder = RedBlack(lukija)
    lukija.readWords()
    finder.addFromReader()
    searchPhrase = "brothers AND ( grimm OR Grimms' )"
    print 'Searching the search phrase "' + searchPhrase + '" in', inputFiles
    tyyppi = Searcher(finder, searchPhrase, lukija)
    print "The status of the search phrase is:", tyyppi.status
    search = sorted(list(tyyppi.search()))
    print "Position(s) in the text where the word was found:"
    print search
    print 'The search returned', len(search), 'unique hits.'
#    print tyyppi.pList

    searchPhrase2 = " human OR ( cat AND mouse )"
    print 'Searching the search phrase "' + searchPhrase2 + '" in', inputFiles
    print "The status of the search phrase is:", tyyppi.status
    search = sorted(list(tyyppi.search(searchPhrase2)))
    print "Position(s) in the text where the word was found:"
    print search
    print 'The search returned', len(search), 'unique hits.'