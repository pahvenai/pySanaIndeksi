__author__="Patrik Ahvenainen"
__date__ ="$1.8.2012 11:42:53$"

from dataHandling import openFile

if __name__ == "__main__":
    print "Class that contains methods for reading words from a file"




class WordReader(object):
    '''
    This class can be used to read words from file.

    Words will be stored in tuple self.words which contains the word and the
    row number in a file where this word appears.
    '''

    chrMap = [] # used internally to map indices to characters
    idxMap = {} # used internally to map characters to indices
    # Any characters added to this list will be accepted:
    acceptedSpecialCharacters = ["-", "'"]


    def __init__(self, filename):
        """
        Upon initializing, there are no words in the word reader
        """
        self.createChrMap()
        self.filename = filename
        self.words = ()
        self.filecount = 0 # preparation for multiple files
        self.wordcount = 0
        self.linecount = 0


    def readWords(self):
        """
        Reads all the words from the file specified in self.filename. Method g
        getWord specifies the accepted word formatting.
        """
        self.fh = openFile(self.filename) # exits on failure
        fileno = 0
        properWords = []

        self.filecount = self.filecount + 1 # preparation for multiple files

        lineno = 0
        for line in self.fh:
            self.linecount = self.linecount + 1
            lineno = lineno + 1

            words = line.split(' ')
            if words == '':
                continue

            for word in words:
                newWord = self.sanitize(word)
                if newWord:
                    properWords.append((newWord, lineno, fileno))
                    self.wordcount = self.wordcount + 1

        self.fh.close()
        self.words = properWords

    def sanitize(self, word):
        """ Returns the sanitized word (remove non-allowed characters) """
        if not word: return None
        newWord = ''
        for letter in word.strip():
            if letter.isalnum() or letter in self.acceptedSpecialCharacters:
                newWord = newWord + letter.upper()
            else:
                break
        return newWord


    def createChrMap(self):
        """
        Creates a list of indices that correspond to characters 0-9, -, A-Z and '.
        A complimentary dict that maps these characters to the same indices is also
        created.
        """

        if self.chrMap:
            return self.chrMap, self.idxMap

        # Create a list to map indices to characters
        i = 1
        for number in range(ord('0'), ord('9')+1): # add numbers 0 to 9
            self.chrMap.append(chr(number))
            i = i + 1
        self.chrMap.append(self.acceptedSpecialCharacters[0]) # add one special character
        i = i + 1
        for letter in range(ord('A'), ord('Z')+1): # add letters A to Z
            self.chrMap.append(chr(letter))
            i = i + 1
        for char in self.acceptedSpecialCharacters[1:]:
            self.chrMap.append(char) # add other special characters
            i = i + 1

        # Create a dict to map characters to indices in the self.chrMap list
        for index, char in enumerate(self.chrMap):
            self.idxMap[char] = index

        return self.chrMap, self.idxMap

    def ind2char(self, index):
        """ Maps indices to characters """
        if not self.chrMap:
            self.createChrMap()
        return(self.chrMap[index])

    def char2ind(self, char):
        """ Maps characters to indices"""
        if not self.chrMap:
            self.createChrMap()
        return(self.idxMap[self.sanitize(char)])

    def getCharMapSize(self):
        ''' Returns the number of different accepted characters '''
        if not self.chrMap:
            createChrMap()
        return len(self.chrMap)

