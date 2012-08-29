# -*- coding: utf-8 -*-
__author__="Patrik Ahvenainen"

# Data handling functions
# openFile(filename, io):   Open file in path for operation io ('r', 'w', etc.)
# closeFile(filehandle):    Close the file with the given filehandle
# getFileNames(mypath):     Return names of files in this path
# printFileList(mypath):    Print on screen the names of files in this path

# imports for data handling purposes
import os
import os.path

if __name__ == "__main__":
    print "This module contains basic file handling functions"

def openFile(path, io='r'):
  '''
  filename must exist
  io can be r for read or w for write
  '''
  try:
      file_handle = open(path, io)
  except IOError:
      if io=='r': stri = 'read from'
      else: stri = 'write to'
      raise IOError("Could not %s file '%s'!" % (stri, path))
      
  return file_handle

def closeFile(filehandle):
    """ Exists only to complement openFile syntax """
    filehandle.close()


def getFileNames(mypath, path=True):
    """
    Returns paths to all files in the given path.
    Set path-flag to False to get the filenames without the (full) path you gave
    """
    fileList= []
    for file in os.listdir(mypath):
        fullPath = os.path.join(mypath,file)
        if os.path.isfile(fullPath):
            if path:
                fileList.append(fullPath)
            else:
                fileList.append(file)
    return fileList

def printFileList(mypath, noPath=True):
    """
    Prints a list containing all files in the given path
    Set noPath-flag to False to get the filenames without the (full) path you 
    gave.
    """
    path = not noPath
    fileList = getFileNames(mypath, path=path)
    for index, file in enumerate(fileList):
        print index, '\t', file
    return fileList