# dataClassifier.py
# -----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

# This file contains feature extraction methods and harness 
# code for data classification

import mostFrequent
import naiveBayes
import perceptron
import samples
import sys
import util
import time as tp
import matplotlib.pyplot as plt
import statistics
import knn
import knn_faces

TEST_SET_SIZE = 15000
DIGIT_DATUM_WIDTH=28
DIGIT_DATUM_HEIGHT=28
FACE_DATUM_WIDTH=60
FACE_DATUM_HEIGHT=70
MAX_ITERATIONS = 10
K_VALUE = 10
TESTING_ITER = 5


def basicFeatureExtractorDigit(datum):
  """
  Returns a set of pixel features indicating whether
  each pixel in the provided datum is white (0) or gray/black (1)
  """
  a = datum.getPixels()

  features = util.Counter()
  for x in range(DIGIT_DATUM_WIDTH):
    for y in range(DIGIT_DATUM_HEIGHT):
      if datum.getPixel(x, y) > 0:
        features[(x,y)] = 1
      else:
        features[(x,y)] = 0
  return features

def basicFeatureExtractorFace(datum):
  """
  Returns a set of pixel features indicating whether
  each pixel in the provided datum is an edge (1) or no edge (0)
  """
  a = datum.getPixels()

  features = util.Counter()
  for x in range(FACE_DATUM_WIDTH):
    for y in range(FACE_DATUM_HEIGHT):
      if datum.getPixel(x, y) > 0:
        features[(x,y)] = 1
      else:
        features[(x,y)] = 0
  return features

def enhancedFeatureExtractorDigit(datum):
  """
  Your feature extraction playground.
  
  You should return a util.Counter() of features
  for this datum (datum is of type samples.Datum).
  
  ## DESCRIBE YOUR ENHANCED FEATURES HERE...
  
  ##
  """
  features =  basicFeatureExtractorDigit(datum)

  "*** YOUR CODE HERE ***"
  
  return features


def contestFeatureExtractorDigit(datum):
  """
  Specify features to use for the minicontest
  """
  features =  basicFeatureExtractorDigit(datum)
  return features

def enhancedFeatureExtractorFace(datum):
  """
  Your feature extraction playground for faces.
  It is your choice to modify this.
  """
  features =  basicFeatureExtractorFace(datum)
  return features

def analysis(classifier, guesses, testLabels, testData, rawTestData, printImage):
  """
  This function is called after learning.
  Include any code that you want here to help you analyze your results.
  
  Use the printImage(<list of pixels>) function to visualize features.
  
  An example of use has been given to you.
  
  - classifier is the trained classifier
  - guesses is the list of labels predicted by your classifier on the test set
  - testLabels is the list of true labels
  - testData is the list of training datapoints (as util.Counter of features)
  - rawTestData is the list of training datapoints (as samples.Datum)
  - printImage is a method to visualize the features 
  (see its use in the odds ratio part in runClassifier method)
  
  This code won't be evaluated. It is for your own optional use
  (and you can modify the signature if you want).
  """
  
  # Put any code here...
  # Example of use:
  for i in range(len(guesses)):
      prediction = guesses[i]
      truth = testLabels[i]
      if (prediction != truth):
          # print ("===================================")
          print ("Mistake on example " , i )
          print ("Predicted %d; truth is %d" % (prediction, truth))
          # print ("Image: ")
          # print (rawTestData[i])
          break


## =====================
## You don't have to modify any code below.
## =====================


class ImagePrinter:
    def __init__(self, width, height):
      self.width = width
      self.height = height

    def printImage(self, pixels):
      """
      Prints a Datum object that contains all pixels in the 
      provided list of pixels.  This will serve as a helper function
      to the analysis function you write.
      
      Pixels should take the form 
      [(2,2), (2, 3), ...] 
      where each tuple represents a pixel.
      """
      image = samples.Datum(None,self.width,self.height)
      for pix in pixels:
        try:
            # This is so that new features that you could define which 
            # which are not of the form of (x,y) will not break
            # this image printer...
            x,y = pix
            image.pixels[x][y] = 2
        except:
            print ("new features:", pix)
            continue
      print (image)

def default(str):
  return str + ' [Default: %default]'

def readCommand( argv ):
  "Processes the command used to run from the command line."
  from optparse import OptionParser  
  parser = OptionParser(USAGE_STRING)
  
  parser.add_option('-c', '--classifier', help=default('The type of classifier'), choices=['mostFrequent', 'nb', 'naiveBayes', 'perceptron','knn'], default='mostFrequent')
  parser.add_option('-d', '--data', help=default('Dataset to use'), choices=['digits', 'faces'], default='digits')
  parser.add_option('-t', '--training', help=default('The size of the training set'), default=100, type="int")
  parser.add_option('-f', '--features', help=default('Whether to use enhanced features'), default=False, action="store_true")
  parser.add_option('-o', '--odds', help=default('Whether to compute odds ratios'), default=False, action="store_true")
  parser.add_option('-1', '--label1', help=default("First label in an odds ratio comparison"), default=0, type="int")
  parser.add_option('-2', '--label2', help=default("Second label in an odds ratio comparison"), default=1, type="int")
  parser.add_option('-w', '--weights', help=default('Whether to print weights'), default=False, action="store_true")
  parser.add_option('-k', '--smoothing', help=default("Smoothing parameter (ignored when using --autotune)"), type="float", default=K_VALUE)
  parser.add_option('-a', '--autotune', help=default("Whether to automatically tune hyperparameters"), default=False, action="store_true")
  parser.add_option('-i', '--iterations', help=default("Maximum iterations to run training"), default=MAX_ITERATIONS, type="int")
  parser.add_option('-s', '--test', help=default("Amount of test data to use"), default=TEST_SET_SIZE, type="int")
  parser.add_option('-q', '--index', help=default("index of data whose predicted label and actual label you want to display"), default = -1, type="int")
  options, otherjunk = parser.parse_args(argv)
  if len(otherjunk) != 0: raise Exception('Command line input not understood: ' + str(otherjunk))
  args = {}
  
  # Set up variables according to the command line input.
  print ("Doing classification")
  print ("--------------------")
  print ("data:\t\t", options.data)
  print ("classifier:\t\t", options.classifier)
  print ("training set size:\t" + str(options.training))
  if(options.data=="digits"):
    printImage = ImagePrinter(DIGIT_DATUM_WIDTH, DIGIT_DATUM_HEIGHT).printImage
    if (options.features):
      featureFunction = enhancedFeatureExtractorDigit
    else:
      print('using basicFeatureExtractorDigit for digits')
      featureFunction = basicFeatureExtractorDigit
  elif(options.data=="faces"):
    printImage = ImagePrinter(FACE_DATUM_WIDTH, FACE_DATUM_HEIGHT).printImage
    if (options.features):
      featureFunction = enhancedFeatureExtractorFace
    else:
      print('using basicFeatureExtractorDigit for faces')
      featureFunction = basicFeatureExtractorFace      
  else:
    print ("Unknown dataset", options.data)
    print (USAGE_STRING)
    sys.exit(2)
    
  if(options.data=="digits"):
    legalLabels = range(10)
  else:
    legalLabels = range(2)
    
  if options.training <= 0:
    print ("Training set size should be a positive integer (you provided: %d)" , options.training)
    print (USAGE_STRING)
    sys.exit(2)
    
  if options.smoothing <= 0:
    print ("Please provide a positive number for smoothing (you provided: %f)" ,options.smoothing)
    print (USAGE_STRING)
    sys.exit(2)
    
  if options.odds:
    if options.label1 not in legalLabels or options.label2 not in legalLabels:
      print ("Didn't provide a legal labels for the odds ratio: (%d,%d)" % (options.label1, options.label2))
      print (USAGE_STRING)
      sys.exit(2)

  if(options.classifier == "mostFrequent"):
    classifier = mostFrequent.MostFrequentClassifier(legalLabels)
  elif(options.classifier == "naiveBayes" or options.classifier == "nb"):
    classifier = naiveBayes.NaiveBayesClassifier(legalLabels)
    classifier.setSmoothing(options.smoothing)
    if (options.autotune):
        print ("using automatic tuning for naivebayes")
        classifier.automaticTuning = True
    else:
        print ("using smoothing parameter k=%f for naivebayes", options.smoothing)
  elif(options.classifier == "perceptron"):
    classifier = perceptron.PerceptronClassifier(legalLabels,options.iterations)
  elif(options.classifier == 'knn'):
    if (options.data == "digits"):
      classifier = knn.KNNClassifier(legalLabels,options.smoothing)
    else:
      classifier = knn_faces.KNNClassifierFaces(legalLabels, options.smoothing)
  else:
    print ("Unknown classifier:", options.classifier)
    print (USAGE_STRING)
    
    sys.exit(2)

  args['classifier'] = classifier
  args['featureFunction'] = featureFunction
  args['printImage'] = printImage
  
  return args, options

USAGE_STRING = """
  USAGE:      python dataClassifier.py <options>
  EXAMPLES:   (1) python dataClassifier.py
                  - trains the default mostFrequent classifier on the digit dataset
                  using the default 100 training examples and
                  then test the classifier on test data
              (2) python dataClassifier.py -c naiveBayes -d digits -t 1000 -f -o -1 3 -2 6 -k 2.5
                  - would run the naive Bayes classifier on 1000 training examples
                  using the enhancedFeatureExtractorDigits function to get the features
                  on the faces dataset, would use the smoothing parameter equals to 2.5, would
                  test the classifier on the test data and performs an odd ratio analysis
                  with label1=3 vs. label2=6
                 """

# Main harness code

def runClassifier(args, options):

  featureFunction = args['featureFunction']
  classifier = args['classifier']
  printImage = args['printImage']
      
  # Load data  
  numTraining = options.training
  numTest = options.test

  if(options.data=="faces"):

    # trr = tp.time()
    numTest = samples.getLabelCount("facedata/facedatatestlabels")
    rawTrainingData, trainingLabels = samples.loadDataAndLabel("facedata/facedatatrain", "facedata/facedatatrainlabels",
                                                           numTraining, FACE_DATUM_WIDTH, FACE_DATUM_HEIGHT)
    rawValidationData, validationLabels = samples.loadDataAndLabel("facedata/facedatatest",
                                                                   "facedata/facedatatestlabels",
                                                                   numTest, FACE_DATUM_WIDTH, FACE_DATUM_HEIGHT)
    rawTestData, testLabels = samples.loadDataAndLabel("facedata/facedatatest", "facedata/facedatatestlabels",
                                                   numTest, FACE_DATUM_WIDTH, FACE_DATUM_HEIGHT)
    # print('time for loading ',numTraining,'  is ',tp.time() - trr)
    # rawTrainingData = samples.loadDataFile("facedata/facedatatrain", numTraining,FACE_DATUM_WIDTH,FACE_DATUM_HEIGHT)
    # trainingLabels = samples.loadLabelsFile("facedata/facedatatrainlabels", numTraining)
    # rawValidationData = samples.loadDataFile("facedata/facedatatrain", numTest,FACE_DATUM_WIDTH,FACE_DATUM_HEIGHT)
    # validationLabels = samples.loadLabelsFile("facedata/facedatatrainlabels", numTest)
    # rawTestData = samples.loadDataFile("facedata/facedatatest", numTest,FACE_DATUM_WIDTH,FACE_DATUM_HEIGHT)
    # testLabels = samples.loadLabelsFile("facedata/facedatatestlabels", numTest)
  else:
    numTest = samples.getLabelCount("digitdata/testlabels")
    rawTrainingData, trainingLabels = samples.loadDataAndLabel("digitdata/trainingimages", "digitdata/traininglabels",
                                                               numTraining, DIGIT_DATUM_WIDTH, DIGIT_DATUM_HEIGHT)
    rawValidationData, validationLabels = samples.loadDataAndLabel("digitdata/validationimages",
                                                                   "digitdata/validationlabels",
                                                                   numTest, DIGIT_DATUM_WIDTH, DIGIT_DATUM_HEIGHT)
    rawTestData, testLabels = samples.loadDataAndLabel("digitdata/testimages", "digitdata/testlabels",
                                                       numTest, DIGIT_DATUM_WIDTH, DIGIT_DATUM_HEIGHT)
    # rawTrainingData = samples.loadDataFile("digitdata/trainingimages", numTraining,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
    # trainingLabels = samples.loadLabelsFile("digitdata/traininglabels", numTraining)
    # rawValidationData = samples.loadDataFile("digitdata/validationimages", numTest,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
    # validationLabels = samples.loadLabelsFile("digitdata/validationlabels", numTest)
    # rawTestData = samples.loadDataFile("digitdata/testimages", numTest,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
    # testLabels = samples.loadLabelsFile("digitdata/testlabels", numTest)
    
  
  # Extract features
  print ("Extracting features...")
  trainingData1 = list(map(featureFunction, rawTrainingData))
  # validationData = map(featureFunction, rawValidationData)
  testData = list(map(featureFunction, rawTestData))
  
  # Conduct training and testing
  print ("Training...")
  classifier.train(trainingData1, trainingLabels, [], validationLabels)
  # print ("Validating...")
  # guesses = classifier.classify(validationData)
  # correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
  # print (str(correct), ("correct out of " + str(len(validationLabels)) + " (%.1f%%).") % (100.0 * correct / len(validationLabels)))
  print ("Testing...")
  guesses = classifier.classify(testData)
  correct = [guesses[i] == testLabels[i] for i in range(len(testLabels))].count(True)
  print (str(correct), ("correct out of " + str(len(testLabels)) + " (%.1f%%).") % (100.0 * correct / len(testLabels)))
  analysis(classifier, guesses, testLabels, testData, rawTestData, printImage)
  
  if options.index!= -1:
    print('predicted label is ',guesses[options.index])
    print('correct label is ',testLabels[options.index])

  # do odds ratio computation if specified at command line
  if((options.odds) & (options.classifier == "naiveBayes" or (options.classifier == "nb")) ):
    label1, label2 = options.label1, options.label2
    features_odds = classifier.findHighOddsFeatures(label1,label2)
    if(options.classifier == "naiveBayes" or options.classifier == "nb"):
      string3 = "=== Features with highest odd ratio of label %d over label %d ===" % (label1, label2)
    else:
      string3 = "=== Features for which weight(label %d)-weight(label %d) is biggest ===" % (label1, label2)    
      
    print (string3)
    printImage(features_odds)

  if((options.weights) & (options.classifier == "perceptron")):
    for l in classifier.legalLabels:
      features_weights = classifier.findHighWeightFeatures(l)
      print ("=== Features with high weight for label %d ==="%l)
      printImage(features_weights)

  return numTraining, correct

def possibleCommands(classifiers, typeData, labelCountFaces, labelCountDigits ):
  dic = {}
  for classifier in classifiers:
    for typeD in typeData:
      dic[(classifier, typeD)] = []

  percents = [ i for i in range(10,101,10)]
  labelCountFacesPercent = [int(t*labelCountFaces/100) for t in percents]
  labelCountDigitsPercent = [int(t * labelCountDigits / 100) for t in percents]

  for classifier in classifiers:
    for typeD in typeData:
      if typeD == 'faces':
        for i in labelCountFacesPercent:
          dicClass = dic[(classifier, typeD)]
          dicClass.append(['-c', classifier, '-d', typeD, '-t', str(i)])
          dic[(classifier, typeD)] = dicClass
      elif typeD == 'digits':
        for i in labelCountDigitsPercent:
          dicClass = dic[(classifier, typeD)]
          dicClass.append(['-c', classifier, '-d', typeD, '-t', str(i)])
          dic[(classifier, typeD)] = dicClass

  return dic

def findValue(key,x):
  typeDir = ''
  for i in x:
    if i == key:
      typeDir = x[x.index(i) + 1]
  return typeDir

def showGraph(x, y1, y2, y3, title, xLabel, yLabel1,yLabel2, yLabel3):
  fig, ax1 = plt.subplots()
  ax2 = ax1.twinx()
  ax3 = ax1.twinx()
  ax1.plot(x, y1, 'g-')
  ax2.plot(x, y2, 'b-')
  ax3.plot(x, y3, 'r-')
  ax1.set_xlabel(xLabel)
  ax1.set_ylabel(yLabel1, color='g')
  ax2.set_ylabel(yLabel2, color='b')
  ax3.set_ylabel(yLabel3, color='r')
  ax3.spines["right"].set_position(("axes", 1.13))
  plt.title(title)
  plt.show()

def fullRun():
  classifiers = ['naiveBayes','knn','perceptron']
  typeData = ['faces', 'digits']
  labelCountFaces = samples.getLabelCount("facedata/facedatatrainlabels")
  labelCountDigits = samples.getLabelCount("digitdata/traininglabels")
  labelCountTestFaces = samples.getLabelCount("facedata/facedatatestlabels")
  labelCountTestDigits = samples.getLabelCount("digitdata/testlabels")
  dic = possibleCommands(classifiers, typeData, labelCountFaces, labelCountDigits )
  for key in dic:
    c2, d2 = key
    values = dic[key]
    percentages, times, stdevs = [], [], []
    for value in values:
      print("===================================")
      print("===================================")
      print("===================================")
      correct, runTime, stdev = runCommand(value)
      percentages.append(correct)
      times.append(runTime)
      stdevs.append(stdev)
      print("===================================")
      print("===================================")
      print("===================================")
    if d2 == 'faces':
      percentages = [ 100 * yy / labelCountTestFaces for yy in percentages ]
    elif d2 == 'digits':
      percentages = [ 100 * yy / labelCountTestDigits for yy in percentages ]
    title = str(c2) + '  ' + str(d2)
    showGraph(range(10, 101, 10), percentages, times, stdevs, title,
              '% of training data', 'accuracy in %', 'time it took for training', 'std dev for % training data')
    print(percentages)
    print(times)
    print(stdevs)

def runCommand(value):
  percentages, times = [], []
  count = TESTING_ITER
  while(count > 0 ):
    startTime = tp.time()
    args, options = readCommand(value)
    numTraining, correct = runClassifier(args, options)
    runTime = tp.time() - startTime
    percentages.append(correct)
    times.append(runTime)
    count = count - 1
  if TESTING_ITER == 1:
    stdev = 0
  else:
    stdev = round(statistics.stdev(percentages), 2)
  percentage = sum(percentages) / len(percentages)
  time = sum(times)/len(times)
  return percentage, time, stdev

if __name__ == '__main__':
  # Read input
  cmdF = sys.argv[1:]
  typeD = 'full'
  for i in cmdF:
    if i == '-type':
      typeD = cmdF[cmdF.index(i) + 1]
      if typeD == 'full':
        fullRun()
        break
    else:
      args, options = readCommand(cmdF)
      runClassifier(args, options)  
      break
