# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$8.8.2012 12:32:57$"

if __name__ == "__main__":
    print "Contains a class for a binary search tool"

from LinkedList import LinkedList # Used as a queue
import linecache # A fancy class for random access text files
import httplib   # For communicating through http (for random word retrieval)
from sys import stdout # for printing without a newline or space ...

class Searcher(object):
    '''
    This class provides a simple set-based searching methods. Searches comprise
    of set operations between individual find-operations for each given word.

    The individual word searches are done with the input object finder using its
    find method for each word. Before word searches, the individual words are
    sanitized with sanitizer or finder's sanitizer using the sanitize method. If
    only a finder is given, its sanitizer holds the filenames of all texts that
    have been indexed. In that case the search function can be used to print the
    search results using file names and to show each line where a hit was found.

    The search supports keywords AND, NOT, OR and XOR corresponding to set
    operations intersection, difference, union and symmetric difference.

    Basic operation:
    searcher = Searcher(finderObject) # initialize
    results = searcher.search("word1 AND word2") # Get the hits from search term

    properties:
    status:     Is 'ok' (string) if current search phrase is ok
    maxHitPrint:Tells how many hits need to be found for lines not to be printed
    public methods:
    search():                  Completes the search and returns the hits
    randomWord():              Fetches a random English word from Internet

    private methods:
    _categorize(words):        Categorizes words according to type
    _checkString():            Checks that the seach phrase is good
    _linesByFiles(results):    Returns the search results sorted by file
    _prettyResults(results):   Prints the results using pretty formatting
    _recursiveSearch(index):   Starting from given index goes through the search
                               string until it finds a closing paranthesis or
                               runs out of search string
    _setOperate(left, right, operation):
                               Does the given set operation to the two sets
    '''



    def __init__(self, finder, searchString, sanitizer=None, maxHitPrint = 10):
        self.str = searchString
        self.finder = finder
        self.sanitizer = sanitizer
        if not sanitizer:
            self.sanitizer = self.finder.lukija
        self.words = searchString.split()
        self.operations = ['AND', 'OR', 'NOT', 'XOR']
        self._maxHitPrint = maxHitPrint # maximum number of lines printed
        self.paranthesis = ['(', ')']
        self._status = 'ok'
        self._checkString() #may flag status as bad
        self.set = set()


##################
### PROPERTIES ###
##################

    def maxHitPrint(self):
        """
        Returns the maximum number of lines printed per file when search
        term is found
        """
        return self._maxHitPrint
    
    def status(self):
        return self._status

######################
### PUBLIC METHODS ###
######################

    def search(self, searchPhrase=None, printPretty = False, maxHitPrint=None,
                     returnCount=False):
        """
        Search the given search phrase using recursive search. If not given uses
        pre-existing search term, if it exists.
        Flags:
        printPretty:    print out hits as pretty as one can
        maxHitPrint:    if you find many terms, print them out less pretty. This
                        value tells you how many is 'many'.
        returnCount:    if set to True, return only the number of hits
        """
        if maxHitPrint:
            self._maxHitPrint = maxHitPrint
        if searchPhrase:
            self.words = searchPhrase.split()
            self._checkString()
        if not self.status() == 'ok':
            return None
        results = self._recursiveSearch(0)
        linesByRows = self._linesByFiles(results)
        if printPretty: self._prettyResults(results, linesByRows)
        if returnCount: return len(results)
        if linesByRows: return linesByRows
        return results


    def randomWord(self, count = 1):
        """
        Returns a random English word fetched from randomword.setgetgo.com
        The count can be set to larger than 1 to get more words.
        """
        conn = httplib.HTTPConnection("randomword.setgetgo.com")
        conn.request("GET", "/get.php")
        r1 = conn.getresponse()
                        # The request returns non-printing characters
        word = r1.read().strip('\xef').strip('\xbb').strip('\xbf').strip()
        if count == 1:
            return word # One word found

        # If we need more than one word, find them here (keep the first word)
        list = [word]
        for _ in range(1, count):
            conn.request("GET", "/get.php")
            r1 = conn.getresponse()
                            # The request returns non-printing characters
            word = r1.read().strip('\xef').strip('\xbb').strip('\xbf').strip()
            list.append( word )
        return list

#######################
### PRIVATE METHODS ###
#######################

    def categorize(self, words):
        """
        Categorize each word to self.types
        Categories are: operations 'O', paranthesis '(' and ')', words 'W' and
        -- if supported by finder -- beginnings of a word (partial words) 'P'.
        """
        self.types = []
        for word in words:
            if word in self.operations:
                self.types.append('O')
            elif word in self.paranthesis:
                self.types.append(word)
            else:
                # last element is a star and reader reads in partial words
                if word[-1] == '*' and self.finder.type() == 'partial':
                    self.types.append('P')
                else:
                    self.types.append('W')

    def _checkString(self):
        """
        The searc term (which is a string) is searched for these things:
            - operator after another operator
            - operator first or last item in search term
            - words with zero letters after sanitation
            - badly placed parantheses
                - closed paranthesis must come after open paranthesis
                - equal number of open and closed parantheses
        The status property is set to 'ok' if search term is good or to 'bad'
        otherwise.

        Creates also a list telling how deep each paranthesis is in inner
        parantheses (in order to find a matching paranthesis).
        For example:
        0    1  0   2   0   0   0   2  0   0   1 0  1   0   0   0   1  # pVal
        word ( word ( word AND word ) NOT word ) or ( word XOR word )  # words
        """
        self.categorize(self.words)
        self._status = 'ok' # will be set to 'bad' if need be

        itemCount = len(self.types)
        paranthesisList = LinkedList() # queue for paranthesis
        self.pList = [0] * len(self.types)
        pVal = 0
        for index, word in enumerate(self.words):
            if self.types[index] == 'W':
                # Words cannot be empty
                if self.sanitizer.sanitize(word) == '':
                    self._status = 'bad'
                    return
            if self.types[index] == 'P':
                # Words cannot be empty, even if they are 'partial'
                if self.sanitizer.sanitize(word) == '':
                    self._status = 'bad'
                    return

            # store paranthesis in a queue, it must be met by closing paranthesis
            if self.types[index] == '(':
                paranthesisList.addLast('(')
                pVal = pVal + 1 # pVal tells how deep we are in paranthesis
                self.pList[index] = pVal
            if self.types[index] == ')':
                self.pList[index] = pVal
                pVal = pVal - 1 # pVal tells how deep we are in paranthesis
                if paranthesisList.values(): # if we had open paranthesis
                    paranthesisList.removeLast() # remove matching one from queue
                else: # we did not have matching paranthesis
                    self._status = 'bad' # Search term is bad
                    return

            # operation cannot be last term, first term or followed by another
            # operation
            if self.types[index] == 'O':
                if index > 0:
                    if not self.types[index-1] == 'O':
                        pass
                else:
                    self._status = 'bad'
                    return
                if index < itemCount - 1:
                    if not self.types[index+1] == 'O':
                        pass
                else:
                    self._status = 'bad'
                    return

        # We have traversed the words. If we have open paranthesis left, they
        # cannot have matching closed paranthesis, search term is bad
        if paranthesisList.values():
            self._status = 'bad'
            return


    def _linesByFiles(self, results):
        """
        Returns a dictionary that has filenames as keys. The values are the row
        numbers. Sorts also the row number list.
        [(687,0), (25,0), (99,1)] -> {'file1': [25, 687], 'file2': [99]}
        """
        if not self.sanitizer == self.finder.lukija:
            return None
        # Make a list of all row numbers found in
        list = {}
        for item in results:
            filename = self.finder.lukija.filenames[item[1]]
            if not filename in list:
                list[filename] = [item[0]]
            else:
                list[filename].append(item[0])
        for file in list:
            list[file] = sorted(list[file])
        return list



    def _prettyResults(self, results, linesByFiles = None):
        """ Prints the search results using pretty formatting """
        # Can only be done if we get filenames from self.finder.lukija
        if not self.sanitizer == self.finder.lukija:
            return None
        if not linesByFiles: # if not yet given, create the list
            linesByFiles = self._linesByFiles(results)

        if not linesByFiles: # empty list
            print 'Search term was not found.'
        else:
            print 'Search terms found:'

        for file in linesByFiles:
            print '  In file "' + file + '":' # print file name
            # if small number of hits, print the entire row for each hit ...
            if len(linesByFiles[file]) <= self.maxHitPrint():
                for line in linesByFiles[file]:
                    print '%s%4d%s%s'  % (' '*4, line, ': ',
                                          linecache.getline(file, line) ),
            # ... and for many hits, print row numbers (many > self.maxHitPrint)
            else:
                print "    on line(s):",
                for line in linesByFiles[file]:
                    if not line == linesByFiles[file][0]: stdout.write(', ')
                    print line, # omit newline
                print # print newline

    def _recursiveSearch(self, index):
        """
        The actual search is done here. Calls recursively itself for each inner
        parantheses. Operations are done to left and right side, where both
        sides are sets and may be a singe search term result, a term in
        parantheses or a current result. Search is done from left to right.
        When we have a left side and a right side, we do a set operation to
        them. If this operation is not given (operator between left and right
        side) we assume the operator to be 'AND'.
        """
        pSkip = 0 # parenthesis skip: this word is handled elsewhere, skip it
        left = None
        right = None
        operator = None
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
            if self.types[index] in ['W', 'P']:
                # whole words; use find method and for ...
                if self.types[index] == 'W':
                    findfunc = self.finder.find
                # ... partial words use findPartial method
                elif self.types[index] == 'P':
                    findfunc = self.finder.findPartial

                results = findfunc(self.words[index], output='list')
                if left == None: # update left side
                    if not results: left = set()
                    else: left = set(results)
                else: # left side exists; update right side
                    if not results: right = set()
                    else: right = set(results)

            # Set the operator tag to the desired operation
            if self.types[index] == 'O':
                operator = self.words[index]
            else:
                # If two sides of the operation exist, operate on them
                if (not left==None) and (not right == None):
                    if not operator: operator = 'AND' # default operator
                    left = self._setOperate(left, right, operator)
                    right = None
                    operator = None

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


