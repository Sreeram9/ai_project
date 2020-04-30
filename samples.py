# samples.py
# ----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import random

## Constants
DATUM_WIDTH = 0 # in pixels
DATUM_HEIGHT = 0 # in pixels

## Module Classes

class Datum:
  """
  A datum is a pixel-level encoding of digits or face/non-face edge maps.

  Digits are from the MNIST dataset and face images are from the 
  easy-faces and background categories of the Caltech 101 dataset.
  
  
  Each digit is 28x28 pixels, and each face/non-face image is 60x74 
  pixels, each pixel can take the following values:
    0: no edge (blank)
    1: gray pixel (+) [used for digits only]
    2: edge [for face] or black pixel [for digit] (#)
    
  Pixel data is stored in the 2-dimensional array pixels, which
  maps to pixels on a plane according to standard euclidean axes
  with the first dimension denoting the horizontal and the second
  the vertical coordinate:
    
    28 # # # #      #  #
    27 # # # #      #  #
     .
     .
     .
     3 # # + #      #  #
     2 # # # #      #  #
     1 # # # #      #  #
     0 # # # #      #  #
       0 1 2 3 ... 27 28
   
  For example, the + in the above diagram is stored in pixels[2][3], or
  more generally pixels[column][row].
       
  The contents of the representation can be accessed directly
  via the getPixel and getPixels methods.
  """
  def __init__(self, data,width,height):
    """
    Create a new datum from file input (standard MNIST encoding).
    """
    DATUM_HEIGHT = height
    DATUM_WIDTH=width
    self.height = DATUM_HEIGHT
    self.width = DATUM_WIDTH
    if data == None:
      data = [[' ' for i in range(DATUM_WIDTH)] for j in range(DATUM_HEIGHT)] 
    # print('data inside datum ',convertToInteger(data))
    # for key,value in convertToInteger(data[10]).items():
    #   print(key,value)
    self.pixels = util.arrayInvert(convertToInteger(data)) 
    
  def getPixel(self, column, row):
    """
    Returns the value of the pixel at column, row as 0, or 1.
    """
    return self.pixels[column][row]
      
  def getPixels(self):
    """
    Returns all pixels as a list of lists.
    """
    return self.pixels    
      
  def getAsciiString(self):
    """
    Renders the data item as an ascii image.
    """
    rows = []
    data = util.arrayInvert(self.pixels)
    for row in data:
      ascii = map(asciiGrayscaleConversionFunction, row)
      rows.append( "".join(ascii) )
    return "\n".join(rows)
    
  def __str__(self):
    return self.getAsciiString()
    


# Data processing, cleanup and display functions
    
def loadDataFile(filename, n,width,height):
  """
  Reads n data images from a file and returns a list of Datum objects.
  
  (Return less then n items if the end of file is encountered).
  """
  DATUM_WIDTH=width
  DATUM_HEIGHT=height
  fin = readlines(filename)
  fin.reverse()
  items = []
  for i in range(n):
    data = []
    for j in range(height):
      if len(fin) == 0:
        break
      data.append(list(fin.pop()))
    if len(data[0]) < DATUM_WIDTH-1:
      # we encountered end of file...
      print ("Truncating at %d examples (maximum)", i)
      break
    items.append(Datum(data,DATUM_WIDTH,DATUM_HEIGHT))
  return items

import zipfile
import os
def readlines(filename):
  "Opens a file or reads it from the zip archive data.zip"
  if(os.path.exists(filename)): 
    return [l[:-1] for l in open(filename).readlines()]
  else: 
    z = zipfile.ZipFile('data.zip')
    return z.read(filename).decode('utf-8').split('\n')

def loadDataAndLabel(filename,filenamelabels, n,width,height):
  items,labels = [], []

  fin = readlines(filename)
  finlabels = readlines(filenamelabels)
  DATUM_WIDTH = width
  DATUM_HEIGHT = height
  fin.reverse()


  lenTest = len([i for i in finlabels if i != ''])
  randomRange = random.sample(range(lenTest),n)

  for line in finlabels:
    if line == '':
      break
    labels.append(int(line))

  # print(fin)
  # print('len test',lenTest)

  for i in range(lenTest):
    data = []
    for j in range(height):
      if len(fin) == 0:
        break
      data.append(list(fin.pop()))
    if len(data[0]) < DATUM_WIDTH - 1:
      # we encountered end of file...
      print("Truncating at %d examples (maximum)", i)
      break
    items.append(Datum(data, DATUM_WIDTH, DATUM_HEIGHT))

  # print('len of items', len(items), 'len of labels',len(labels))
  itemsNew, labelsNew = [], []
  for i in randomRange:
    itemsNew.append(items[i])
    labelsNew.append(labels[i])

  return itemsNew,labelsNew

def getLabelCount(filenamelabels):
  finlabels = readlines(filenamelabels)
  lenTest = len([i for i in finlabels if i != ''])
  return lenTest

def loadLabelsFile(filename, n):
  """
  Reads n labels from a file and returns a list of integers.
  """
  fin = readlines(filename)
  labels = []
  for line in fin[:min(n, len(fin))]:
    if line == '':
        break
    labels.append(int(line))
  return labels
  
def asciiGrayscaleConversionFunction(value):
  """
  Helper function for display purposes.
  """
  if(value == 0):
    return ' '
  elif(value == 1):
    return '+'
  elif(value == 2):
    return '#'    
    
def IntegerConversionFunction(character):
  """
  Helper function for file reading.
  """
 
  if(character == ' '):
    return 0
  elif(character == '+'):
    return 1
  elif(character == '#'):
    return 2    

def convertToInteger(data):
  """
  Helper function for file reading.
  """
  # print('Inside convertToInteger data is ',data)
  # if type(data) != type([]):
  #   print('Inside If convertToInteger')
  #   return IntegerConversionFunction(data)
  # else:
  #   print('Inside else convertToInteger')
  #   return map(convertToInteger, data)
  result = [[' ' for i in range(0,len(data[0]))] for j in range(0,len(data))] 
  # print('length of outer',len(data))
  # print('length of inner',len(data[0]),len(data[1]))
  for outer in range(0,len(data)):
    for inner in range(0,len(data[outer])):
      result[outer][inner] = IntegerConversionFunction(data[outer][inner])

  return result
# Testing

def _test():
  import doctest
  doctest.testmod() # Test the interactive sessions in function comments
  n = 1000000
#  items = loadDataFile("facedata/facedatatrain", n,60,70)
#  labels = loadLabelsFile("facedata/facedatatrainlabels", n)
  # items = loadDataFile("digitdata/trainingimages", 1000000,28,28)
  # print('length of items ',len(items))
  labels = loadLabelsFile("digitdata/traininglabels", n)
  # print('items are ',items)
  # print('labels are ',labels)
  for i in range(0,len(labels)):
    print ('item is ',labels[i])
    # print (items[i])
    # print (items[i].height)
    # print (items[i].width)
    # # print (dir(items[i]))
    # print (items[i].getPixels())

if __name__ == "__main__":
  _test()  
