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
  Opens the file in the given path in read mode if param io is not given

  @param io: string 'r' for read and string 'w' for write
  @type io: string
  @return: file handle
  '''
  try:
      file_handle = open(path, io)
  except IOError:
      if io=='r': stri = 'read from'
      else: stri = 'write to'
      raise IOError("Could not %s file '%s'!" % (stri, path))
      
  return file_handle

def closeFile(filehandle):
    """
    Exists only to complement openFile syntax
    @param filehandle: filehandle to be closed
    """
    filehandle.close()


def getFileNames(mypath, path=True):
    """
    Returns paths to all files in the given path. Returns an empty list on
    error, does not raise exceptions.

    @param mypath: The directory whose files are returned
    @type mypath: string, name of a directory
    @param path: value False means you don't want filenames listed with the
                 given path
    @type path: boolean
    @return: a list of files in the directory (if any)
    """
    fileList= []
    if not os.path.isdir(mypath):
        return fileList
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
    Prints a list containing all files in the given path. File list is obtained
    with getFileNames. Returns also the list of files returned by getFileNames.

    @param noPath: value True means you don't want filenames listed with the
                   given path
    @type noPath: boolean
    @return: a list of the files returned by getFileNames
    """
    path = not noPath
    fileList = getFileNames(mypath, path=path)
    for index, file in enumerate(fileList):
        print index, '\t', file
    return fileList