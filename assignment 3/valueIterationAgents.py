# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
from argparse import Action

class ValueIterationAgent(ValueEstimationAgent):
    
    
    
    """ creates a new grid based on the passed grid and returns it """
    def copyGrid(self, grid):
        newGrid={};
        for key in grid.keys():
            newGrid[key]=grid[key]
        return newGrid
    
    
    
    
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        
        
        
        """ does value iteration, keeps the previous board and generates the next
        board based on it, counts V values for each state"""
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()
        states=mdp.getStates()
        previousGrid=util.Counter() 
        for i in range(iterations):
            curGrid=self.copyGrid(previousGrid)
            for state in states:
                if self.mdp.isTerminal(state):
                    curGrid[state]=0
                else:
                    mxAction=-1000000000000
                    actions=self.mdp.getPossibleActions(state)
                    for action in actions:
                        transitions=self.mdp.getTransitionStatesAndProbs(state, action)
                        actionSum=0
                        for transition in transitions:
                            nextstate=transition[0]
                            prob=transition[1]
                            reward=self.mdp.getReward(state, action, nextstate)
                            actionSum+=prob*reward+prob*discount*previousGrid[nextstate]
                        mxAction=max(mxAction, actionSum)
                    curGrid[state]=mxAction
            previousGrid=curGrid
        self.values=previousGrid
                    
                 
            
            
            


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        
        """ computes Q values using V values, sums up for each transition and returns it"""
        transitions=self.mdp.getTransitionStatesAndProbs(state, action)
        sum=0
        for transition in transitions:
            nextstate=transition[0]
            reward=self.mdp.getReward(state, action, nextstate)
            prob=transition[1]
            sum+=prob*(reward+self.discount*self.values[nextstate])
        return sum

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        """ returns the best action in the current state, which will be included
        in the policy"""
        res=None
        actions=self.mdp.getPossibleActions(state)
        mx=-1000000000
        for action in actions:
            curRes=self.computeQValueFromValues(state, action)
            if curRes>mx:
                mx=curRes;
                res=action
        return res
            
        
            

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
