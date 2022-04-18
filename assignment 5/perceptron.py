# perceptron.py
# -------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Perceptron implementation
import util
PRINT = True

class PerceptronClassifier:
    """
    Perceptron classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "perceptron"
        self.max_iterations = max_iterations
        self.weights = {}
        for label in legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def setWeights(self, weights):
        assert len(weights) == len(self.legalLabels);
        self.weights = weights;

    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        """
        The training loop for the perceptron passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        See the project description for details.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        (and thus represents a vector a values).
        """
        
        import numpy as np

        self.features = trainingData[0].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.
        
        
        for i in range(len(self.legalLabels)):
            for j in range(len(self.features)):
                self.weights[i][self.features[j]]=0
            
        
        
        """ i didn't use the classify method and implemented it by myself """
        
        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for i in range(len(trainingData)):
                "*** YOUR CODE HERE ***"
                mx=-1
                label=-1;
                data=trainingData[i]
                for j in range(len(self.legalLabels)):
                    sum=0
                    ws=self.weights[self.legalLabels[j]]
                    for key in ws.keys():
                        sum+=data[key]*ws[key]
                    if(sum>mx):
                        mx=sum
                        label=self.legalLabels[j]
                if(label!=trainingLabels[i]):
                    for key in self.weights[label].keys():
                        self.weights[label][key]-=data[key]
                    for key in self.weights[trainingLabels[i]].keys():
                        self.weights[trainingLabels[i]][key]+=data[key]
                    
                    
                                        

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


    def findHighWeightFeatures(self, label):
        """
        Returns a list of the 100 features with the greatest weight for some label
        """
        import operator
        featuresWeights = []

        "*** YOUR CODE HERE ***"
        ws=self.weights[label]
        sorted_x = sorted(ws.items(), key=operator.itemgetter(1))
        for i in range(100):
            if len(sorted_x)-i>=0:
                featuresWeights.append(sorted_x[len(sorted_x)-i][0])
        print featuresWeights
        return featuresWeights
