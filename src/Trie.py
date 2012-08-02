# To change this template, choose Tools | Templates
# and open the template in the editor.

from Puu import Puu
from WordReader import getCharMapSize, char2ind, ind2char, getWord
import random

__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 12:16:17$"

if __name__ == "__main__":
    print "Contains a class for Trie-tree"

# egrep "( sana|^sana)" *.txt -i --count
# egrep "( sana|^sana)" *.txt -ni

class Trie(Puu):
    '''
    A Trie-type tree that can hold words containing alphanumerals and the '-'-
    character.
    '''



    def __init__(self):
        self.root = None

    def add(self, object):
        '''
        Adds a new word to the tree.
        '''
        if self.root == None:
            self.root = TrieBranch()
        self.addBranch(object)

    def find(self, word, type='startswith'):
        '''
        Tries to find the asked word from the tree. Returns a number indicating
        the file and a file number for each found instance. Can be used to find
        exact matches or the beginnings of the words. Uses recursion to travel
        in the trie-tree.
        '''

        word = getWord(word) # check that we have no illegal characters
        # find this word in the tree recursively and return positions of all the
        # instances
        positions = self.findRecursive(word, 1, type, self.root)

        if positions: #found
            count = len(positions)
            linecount = len(set(positions))
        else: #did not find the word
            count = 0; linecount = 0
        return positions, count, linecount


    def findRecursive(self, word, charNo, type, branch):
        """
        First we check that a required letter exist in the tree. If not, we did
        not find the word. If we find it and it's the last letter to find,
        return the instances where this word was found. If it's not the last
        letter move on recursively to the next letter.
        """
        char = word[charNo-1]
        index = char2ind(char)

        if not branch.children[index]:
            return None # Required letter not found
        else:
            # if the next letter is the last letter, we found our letter
            if charNo == len(word):
                if type == 'exact':
                    return branch.children[index].exact
                else:
                    return branch.children[index].match

            return self.findRecursive(word, charNo+1, type, branch.children[index])

    def addBranch(self, object, charNo = 0, branch = 'root'):
        '''
        Add one branches until whole word is added.
        '''
        word = object[0]
        letter = word[charNo]
        index = char2ind(letter)

        if branch == 'root': 
            branch = self.root

        exact = False
        if charNo == len(word) - 1:
            exact = True

        branchExists = branch.children[index] # Empty list means no such branch

        if not branchExists:
            # create a new branch and add it to the tree
            newBranch = TrieBranch(object, exact)
            branch.children[index] = newBranch
            nextBranch = newBranch # tree may continue here
        else:
            # branch exists, update only the newly found position to the branch
            branch.updateBranch(object, exact)
            nextBranch = branch.children[index] # tree may continue here

        # If not the last letter in the word, continue recursively
        if not exact:
            charNo = charNo + 1
            self.addBranch(object,charNo,nextBranch)
        pass
    

    def printRandomRoute(self):
        """
        Prints a random route from root to leaf.
        """
        
        parent = self.root
        word = ''
        lastindex = None
        while(True):
            if not parent == None:
                if parent.children:
                    lastindex = None
                    indices = []
                    for index, child in enumerate(parent.children):
                        if child:
                            print word + ind2char(index), 
                            indices.append(index)
                            lastindex = index
                    if lastindex == None:
                        break
                    else:
                        lastindex = random.choice(indices)
                        parent = parent.children[lastindex]
                    print '; route: ', ind2char(lastindex), ' found n=', \
                          len(parent.match), ' (', len(set(parent.match)), \
                          'lines) @ ', parent.match
                    word = word + ind2char(lastindex)


class TrieBranch(object):
    '''
    Contains the information of one branch.
    '''

    NO_DIFF_CHARS = 0

    def __init__(self, object = '', exact = False):
        self.exact = []
        self.match = []
        if object:
            self.updateBranch(object, exact)
        if TrieBranch.NO_DIFF_CHARS == 0:
            TrieBranch.NO_DIFF_CHARS = getCharMapSize()
        self.children = [None] * (TrieBranch.NO_DIFF_CHARS)


    def updateBranch(self, object, exact):
        """ Add position info for this object """
        self.match.append(object[1:3])
        if exact:
            self.exact.append(object[1:3])