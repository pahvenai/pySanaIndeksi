# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"
__date__ ="$10.8.2012 11:55:42$"

import DataHandling
import unittest

class  PyDataHandlingTestCases(unittest.TestCase):

    def testRaisesError(self):
       self.assertRaises(IOError, DataHandling.openFile, 'Non-existing_file', 'r')

    def testOpensFile(self):
       filu = DataHandling.openFile( 'DataHandlingUnitTest.py', 'r')
       DataHandling.closeFile(filu)

    def testFileList(self):
        filesInThisPath = DataHandling.getFileNames('.', path = False)
        self.assertTrue('DataHandlingUnitTest.py' in filesInThisPath,
                        'DataHandling: Did not find find files')


def suite():
    return unittest.makeSuite(PyDataHandlingTestCases,'test')


# Create unit tests

if __name__ == "__main__":
    print "Running unit tests for DataHandling module"
    runner = unittest.TextTestRunner()
    runner.run(suite())