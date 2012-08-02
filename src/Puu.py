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

    def add( self, item):
        raise NotImplementedError( "Adding not implemented" )

    def find( self, item, type):
        raise NotImplementedError( "Finding not implemented" )


