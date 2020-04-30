# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import classificationMethod
import math
from operator import itemgetter
from collections import Counter

class KNNClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels,k):
    self.legalLabels = legalLabels
    self.type = "knn"
    self.k = k # this is the value of k for the KNN algorithm, ** use it in your train method **
    self.trainingData = []
    self.trainingLabels = []
    
      
  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    # print('training data is',list(trainingData))
    
    for datum,correctLabel in zip(trainingData,trainingLabels):
      self.trainingData.append(datum)
      self.trainingLabels.append(correctLabel)
     
   
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
  def getFreq(self, datum1):
    frequency = Counter()
    distances = []
    # print('datum1 is ',datum1)
    for datum2, label in zip(self.trainingData, self.trainingLabels):
      dist = self.getDistance(datum1, datum2)
      distances.append((dist, label))
    # print(' distances are ',distances)
    sorted_distances = sorted(distances, key=itemgetter(0))[0:int(self.k)]
    # print(' distances are ',sorted_distances)
    for dis in sorted_distances:
      frequency[dis[1]] = frequency[dis[1]] + 1
    # print('Highest frequency label is ',frequency.most_common(1)[0][0])
    return frequency.most_common(1)[0][0]

  def classify(self, testData):
    """
   
    """
    print('value of k ',self.k)
    import multiprocessing
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_cores)

    guesses = pool.map(self.getFreq,testData )

    # print('The first k are ',sorted_distances[0:int(self.k)])
    # print('frequency map is ',frequency)
    # print('Highest frequency label is ',frequency.most_common(1)[0][0])
    # print('value of k is ',self.k) 
    # print('The most common are ',sorted_distances.most_common(k))
    return guesses

  def getDistance(self,point1,point2):
    difference = point1 - point2
    sum = 0
    for value in difference.values():
        sum = sum + value * value
    return math.sqrt(sum)
    

    
      
