__author__="Patrik Ahvenainen"
__date__ ="$31.7.2012 18:12:31$"

if __name__ == "__main__":
    print "This is an abstract class"

class Puu(object):
    """
    This is an abstract class. Classes that inherit from this class should have
    implementation for adding an item to a tree and finding an item from a tree.
    This class is not strictly speaking necessary but it makes sure your tree
    classes are working properly.
    """

    #@accepts(Puu, String, object)
    def add(self, key, value):
        """
        This method is used to add items to the tree. Each item contains a key
        which should be a string and an arbitrary value corresponding to that
        key.
        """
        raise NotImplementedError( "Adding not implemented" )

    #@accepts(Puu, String)
    #@returns(list, int, int)
    def find(self, key):
        """
        Finds the key from the tree. If the key is found return the following:
        1:  A list of positions where this word was found
        2:  Number of found instances
        3:  Number of lines where the word was found
        """
        raise NotImplementedError( "Finding not implemented" )


