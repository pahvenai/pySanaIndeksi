# -*- coding: utf-8 -*-
# Data handling functions

from sys import exit
import os
import os.path

if __name__ == "__main__":
    print "This module contains basic file handling functions"

def openFile(filename, io='r'):
  '''
  filename must exist
  io can be r for read or w for write
  '''
  try:
      file_handle = open(filename, io)
  except:
      if io=='r': stri = 'read from'
      else: stri = 'write to'
      print "ERROR: Could not %s file %s!" % (stri, filename)
      exit()
      
  return file_handle

def closeFile(filehandle):
    filehandle.close()


def getFileNames(mypath, path=True):
    """ Returns paths to all files in the given path """
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
    """ Prints a list containing all files in the given path """
    path = not noPath
    fileList = getFileNames(mypath, path=path)
    for index, file in enumerate(fileList):
        print index, '\t', file
    return fileList