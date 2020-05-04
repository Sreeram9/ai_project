# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import classificationMethod
import math
from collections import Counter


class KNNClassifierFaces(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.

  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """

  def __init__(self, legalLabels, k):
    self.legalLabels = legalLabels
    self.type = "knn"
    self.k = 50  # this is the value of k for the KNN algorithm, ** use it in your train method **
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
    self.trainingLabels = trainingLabels
    self.trainingData = trainingData

    "*** YOUR CODE HERE ***"

  def classify(self, testData):
    """

    """
    print('value of k ', self.k)
    import multiprocessing
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_cores)
    guesses = pool.map(self.getFreq, testData)
    return guesses

  def getFreq(self, datum1):

    distances = list(map(lambda x: ( self.cosineDistance(x[1],datum1), self.trainingLabels[x[0]]),
             enumerate(self.trainingData)))

    sorted_distances = (sorted(distances, key=lambda x: x[0]))[:int(self.k)]
    r = Counter([ label for (_,label) in sorted_distances])
    return r.most_common(1)[0][0]



  def getDistance(self, point1, point2):
    difference = point1 - point2
    return math.sqrt(sum(map(lambda x: x * x, difference.values())))

  def cosineDistance(self, pt1, pt2):
    a, b, c = 0, 0, 0
    for key in pt1:
      if key in pt2:
        t1 = pt1[key]
        t2 = pt2[key]
        a += t1 * t1
        b += t2 * t2
        c += t1 * t2
    return 1 - (c / math.sqrt(a * b))




