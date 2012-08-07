# To change this template, choose Tools | Templates
# and open the template in the editor.

from Puu import Puu
from WordReader import WordReader
from LinkedList import LinkedList
import random

__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 12:16:17$"

if __name__ == "__main__":
    print "Contains a class for Trie-tree"

# egrep "( sana|^sana)" *.txt -i --count
# egrep "( sana|^sana)" *.txt -ni

class Trie(Puu):
    '''
    A Trie-type tree that can hold words containing alphanumerals, hyphens and
    aposthrophes. The WordReader module handles in reality the the word
    sanitizing.

    A trie instance is tied to its WordReader object: it gets the size of the
    child node list from it and the mapping of characters to indices in that
    list.
    '''



    def __init__(self, wordreader):
        self.root = None
        self.lukija = wordreader
        self.charMapSize = self.lukija.getCharMapSize()

    def add(self, key, value):
        '''
        Adds a new word to the tree. The addítion is done via recursive addNode
        function.
        '''
        if self.root == None:
            self.root = TrieNode(self.charMapSize)
        self.addNode(key, value)

    def find(self, word, type='startswith'):
        '''
        Tries to find the asked word from the tree. Can be used to find
        exact matches or the beginnings of the words. Uses recursion to travel
        in the trie-tree. Returns a list of the positions where that word was
        found (if any), the number of found instances and the number of
        different line where that word was found.

        The word is first sanitized.
        '''

        word = self.lukija.sanitize(word) # check that we have no illegal characters
        # find this word in the tree recursively and return positions of all the
        # instances
        positions = self.findRecursive(word, 1, type, self.root)

        if positions: #found
            count = len(positions)
            linecount = len(set(positions))
        else: #did not find the word
            count = 0; linecount = 0
        return positions, count, linecount


    def findRecursive(self, word, charNo, type, node):
        """
        First we check that a required letter exist in the tree. If not, we did
        not find the word. If we find it and it's the last letter to find,
        return the instances where this word was found. If it's not the last
        letter move on recursively to the next letter.
        """
        char = word[charNo-1]
        index = self.lukija.char2ind(char)

        if not node.children[index]:
            return None # Required letter not found
        else:
            # if the next letter is the last letter, we found our letter
            if charNo == len(word):
                if type == 'exact':
                    return node.children[index].exact.values()
                else:
                    return node.children[index].match.values()

            return self.findRecursive(word, charNo+1, type, node.children[index])




    def addNode(self, key, value, charNo = 0, node = 'root'):
        '''
        Add a node at a time until the whole word is added. Each node represents
        a letter of that word.
        '''
        letter = key[charNo]
        index = self.lukija.char2ind(letter)

        if node == 'root':
            node = self.root

        exact = False
        if charNo == len(key) - 1:
            exact = True

        nodeExists = node.children[index] # Empty list means no such branch

        if nodeExists:
            # branch exists, update only the newly found position to the branch
            node.updateNode(value, exact)
            nextNode = node.children[index] # tree may continue here
        else:
            # create a new branch and add it to the tree
            newNode = TrieNode(self.charMapSize, value, exact)
            node.children[index] = newNode
            nextNode = newNode # tree may continue here

        # If not the last letter in the word, continue recursively
        if not exact:
            charNo = charNo + 1
            self.addNode(key, value ,charNo,nextNode)
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
                            print word + self.lukija.ind2char(index),
                            indices.append(index)
                            lastindex = index
                    if lastindex == None:
                        break
                    else:
                        lastindex = random.choice(indices)
                        parent = parent.children[lastindex]
                    print '; route: ', self.lukija.ind2char(lastindex), ' found n=', \
                          parent.match.count, ' (', len(set(parent.match.values())), \
                          'lines) @ ', parent.match.values()
                    word = word + self.lukija.ind2char(lastindex)


class TrieNode(object):
    '''
    Contains the information of one node. It contains two lists of the positions
    where the string corresponding to that node is found. One stores only the
    positions of exact matches and the other all words that start with that
    string.

    Child maintenance is handled with a minimum list. A new TrieNode is given
    the maximum amount of children (number of acceptable characters).

    self.updateNode(value, exact):
        Adds the value to the value lists of that node. Exact-flag determines
        whether the value is added also to the list of exact matches.
    '''

    def __init__(self, charMapSize, value = '', exact = False):
        """
        Trie node contains two linked lists for its values: one is intended for
        exact matches (it is updated only with exact-flag raised). Upon
        creation, the minimum list type child list is created for that node.
        """
        self.exact = LinkedList()
        self.match = LinkedList()
        if value:
            self.updateNode(value, exact)
        self.children = [None] * (charMapSize)


    def updateNode(self, position, exact):
        """ Add position info for this object """
        self.match.addLast(position)
        if exact:
            self.exact.addLast(position)