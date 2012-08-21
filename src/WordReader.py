# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$1.8.2012 11:42:53$"

from DataHandling import openFile

if __name__ == "__main__":
    print "Class that contains methods for reading words from a file"




class WordReader(object):
    '''
    This class can be used to read words from one or multiple files. The file 
    names are given to the object upon initialization.

    Words will be stored in tuple self.words which contains the word and the
    row number in a file where this word appears and the file number.

    Accepted characters are determined when a new WordReader object is created.
    The case can be lower, upper or mixed. For lower and upper case only all
    letters are converted to lower and upper case, respectively. Numerals are
    accepted by default but can be excluded. Letters are from A to Z and any
    other letters and non alphanumerical characters can be passed in to the
    reader via specialCharacters.
    
    Characters can be mapped to an indexed table via char2ind() function.

    methods:

    self.addFileName(filename)      Add a new file by giving its filename.
    self.addFileNames(filenames):   Add multiple files by giving a list
                                    containing their filenames.
    self.char2ind(char)             Returns the index corresponding to character
    self.clear()                    Forget any read words
    self.clearFileNames()           Empties the filename list
    self.getCharMapSize()           Returns the number of accepted characters
    self.ind2char(index)            Returns the character corresponding to index
    self.readWords()                Reads all words with accepted characters
                                    from all files.
    self.sanitize(word)             Removes non-accepted characters from the word

    private methods:
    self._createChrMap()            Creates the character-index-character
                                    mapping.
    '''


    def __init__(self, filenames = [], specialCharacters = ["-", "'"],
                 acceptNumerals = True, acceptUpperCase = True,
                 acceptLowerCase = False):
        """
        Upon initializing, there are no words in the WordReader.
        During initialization accepted characters are mapped. They are
        - all characters in the specialCharacters list
        - numerals if acceptNumerals equals True
        - upper case letters if acceptUpperCase equals True
        - lower case letters if acceptLowerCase equals True.
        If only one case is accepted all letters are considered to be of that
        case.

        Filenames list the names of the files from which the words are read.
        They must be in a list form. After initialization new files can be added
        with addFileName(...) and addFileNames(...).
        """
        self.chrMap = [] # used internally to map indices to characters
        self.idxMap = {} # used internally to map characters to indices
        # Any characters added to this list will be accepted:
        self.acceptedSpecialCharacters = specialCharacters
        self.numerals = acceptNumerals
        if acceptUpperCase and acceptLowerCase:
            self.case = 'mixed'
        elif acceptUpperCase and not acceptLowerCase:
            self.case = 'upper'
        elif not acceptUpperCase and acceptLowerCase:
            self.case = 'lower'
        else:
            self.case = 'none'
        self._createChrMap()

        self.filenames = filenames
        self.clear()

###############
### METHODS ###
###############

    def addFileName(self, filename):
        self.filenames.append(filename)
    def addFileNames(self, filenames):
        for filename in filenames:
            self.filenames.append(filename)

    def char2ind(self, char):
        """ Maps characters to indices"""
        if not self.chrMap:
            self._createChrMap()
        return(self.idxMap[self.sanitize(char)])

    def clear(self, type='empty'):
        """ Clears any words read so far """
        self.words = []
        self.filecount = 0 
        self.wordcount = 0
        self.linecount = 0
        self.readCount = 0
        if type == 'all':
            self.clearFileNames()
            
    def clearFileNames(self):
        self.filenames = []

    def getCharMapSize(self):
        ''' Returns the number of different accepted characters '''
        if not self.chrMap:
            _createChrMap()
        return len(self.chrMap)

    def ind2char(self, index):
        """ Maps indices to characters """
        if not self.chrMap:
            self._createChrMap()
        return(self.chrMap[index])

    def readWords(self):
        """
        Reads all the words from the file specified in self.filenames. Method
        sanitize specifies the accepted word formatting.
        """

        for index, filename in enumerate(self.filenames):
            if self.readCount > index:
                continue
            self.readCount = self.readCount + 1
            self.fh = openFile(filename) # exits on failure

            lineno = 0
            for line in self.fh:
                self.linecount = self.linecount + 1
                lineno = lineno + 1

                words = line.split()
                if words == '':
                    continue

                for word in words:
                    newWord = self.sanitize(word)
                    if newWord:
                        self.words.append((newWord, lineno, self.filecount))
                        self.wordcount = self.wordcount + 1

            self.fh.close()
            self.filecount = self.filecount + 1 # preparation for multiple files


    def sanitize(self, word):
        """ Returns the sanitized word (remove non-allowed characters) """
        if not word: return None

        newWord = ''
        # We traverse the word a letter at a time until we hit non-allowed chars
        for letter in word.strip():
            if letter in self.acceptedSpecialCharacters:
                newWord = newWord + letter

            elif letter.isalpha():
                if self.case == 'none':
                    break;
                elif self.case == 'mixed':
                    newWord = newWord + letter
                elif self.case == 'upper':
                    newWord = newWord + letter.upper()
                elif self.case == 'lower':
                    newWord = newWord + letter.lower()

            elif letter.isdigit() and self.numerals:
                newWord = newWord + letter

            else: # Bad character, end reading the word here
                break
        return newWord # newWord may be an empty string



#######################
### PRIVATE METHODS ###
#######################

    def _createChrMap(self):
        """
        Creates a list of indices that correspond to accepted characters.
        A complimentary dict that maps these characters to the same indices is also
        created.
        """

        if self.chrMap:
            return self.chrMap, self.idxMap

        if self.numerals:
            # Create a list to map indices to characters
            for number in range(ord('0'), ord('9')+1): # add numbers 0 to 9
                self.chrMap.append(chr(number))

        self.chrMap.append(self.acceptedSpecialCharacters[0]) # add one special character

        if self.case in ['mixed', 'lower']:
            for letter in range(ord('a'), ord('z')+1): # add letters a to z
                self.chrMap.append(chr(letter))
        if self.case in ['mixed', 'upper']:
            for letter in range(ord('A'), ord('Z')+1): # add letters A to Z
                self.chrMap.append(chr(letter))

        for char in self.acceptedSpecialCharacters[1:]:
            self.chrMap.append(char) # add other special characters

        # Create a dict to map characters to indices in the self.chrMap list
        for index, char in enumerate(self.chrMap):
            self.idxMap[char] = index

        return self.chrMap, self.idxMap