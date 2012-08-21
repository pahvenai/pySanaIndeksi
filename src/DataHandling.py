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


def getFileNames(mypath):
    """ Returns paths to all files in the given path """
    fileList= []
    for file in os.listdir(mypath):
        fullPath = os.path.join(mypath,file)
        if os.path.isfile(fullPath):
            fileList.append(fullPath)
    return fileList

def printFileList(mypath):
    """ Prints a list containing all files in the given path """
    fileList = getFileNames(mypath)
    for index, file in enumerate(fileList):
        print index, '\t', file