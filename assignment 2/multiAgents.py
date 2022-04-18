# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from Tkconstants import CURRENT
from mysql.connector.errorcode import ER_INSECURE_CHANGE_MASTER

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        """counts minimal distance to the food and to the ghosts, returns more value if
        food is nearer or ghost farther. the main quantity which measures the values is 
        10/minfood-10/minghost, (minfood-distance to food, minghost-distance to ghost), of course
        it's checked whether the distance is zero in order not to encounter zero division"""
        foodList = newFood.asList()
        minFood = 1000000;
        minGhost = 1000000;
        result = successorGameState.getScore()
        for food in foodList:
            minFood = min(minFood, (manhattanDistance(newPos, food)))
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            minGhost = min(minGhost, manhattanDistance(newPos, ghostPos))
        if(minFood!=0):
            result+=10.0/(minFood)
        if(minGhost!=0):
            result-=10.0/(minGhost)
        return result

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    
        
        
        
    """ generates all possible configurtions of ghosts on a board and keeps them"""
    def generateActions(self, gameState, ind, states, num):
        if(ind==num or gameState.isWin() or gameState.isLose()):
            states.append(gameState)
            return
        else:
            actions=gameState.getLegalActions(ind)
            for action in actions:
                newGameState=gameState.generateSuccessor(ind, action)
                self.generateActions(newGameState, ind+1, states, num)
        
    
    
    """this is a minimizer for ghost actions, it chooses the minimal value that can
    be achieved from their actions and returns it"""    
    def min_value(self, gameState, depth, initialDepth):
        if(gameState.isLose() or depth==0 or gameState.isWin()):
            curRes=self.evaluationFunction(gameState)
            return curRes
        states=[]
        num=gameState.getNumAgents()
        self.generateActions(gameState, 1, states, num)
        res=10000000
        for state in states:
            curRes=self.max_value(state, depth-1, initialDepth)
            if(curRes<res):
                res=curRes
        return res
        
        
        
    
    """ this is a maximizer for determining pacman actions. It chooses the best
    option for him to maximize his utility, if it's the roo of the minimax tree this method returns
    an optimal action, initialDepth here means left depth"""
    def max_value(self, gameState, depth, initialDepth):
        if(gameState.isLose() or depth==0 or gameState.isWin()):
            curRes=self.evaluationFunction(gameState)
            return curRes
        actions=gameState.getLegalActions(0)
        res=-100000;
        resAction='Center'
        for action in actions:
            newGameState=gameState.generateSuccessor(0, action)
            curRes=self.min_value(newGameState, depth, initialDepth)
            if(curRes>res):
                resAction=action;
                res=curRes
        if depth==initialDepth:
            return resAction
        else: return res
        
        

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState, self.depth, self.depth)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

         

            
        
    """ unlike the above min_value, this one generates only necessary number of
    successor states, improved with recursive approach. Here ghosts take actions
    one by one and compare the values to their maximizer's, if it's less than
    alpha then there's no reason for further exploring because the value in maximizer can't be improved"""
    def min_value(self, ind, num, gameState, depth,initialDepth, alpha, beta):
        if(gameState.isLose() or depth==0 or gameState.isWin()):
            curRes=self.evaluationFunction(gameState)
            return curRes
        v=1000000000
        if ind==num:
             v=min(v, self.max_value(gameState, depth-1, initialDepth, alpha, beta))
             if v<alpha:
                return v
        else:
            actions=gameState.getLegalActions(ind)
            curbeta=beta
            for i in range(len(actions)):
                    newGameState=gameState.generateSuccessor(ind, actions[i])
                    v=min(v, self.min_value(ind+1, num, newGameState, depth, initialDepth, alpha, curbeta))
                    if v<alpha:
                        return v
                    curbeta=min(curbeta, v)
        return v
        
        
        
    """ this is a maximizer for pacman actions. If it's the root of the tree then
    pacman just chooses the best option and the best direction and doesn't pay attention to beta values as
    the root doesn't have ancestors, otherwise if the current returned value for a
    particular action is greater then beta beta, there is no reason for further
    exploring"""
    def max_value(self, gameState, depth, initialDepth, alpha, beta):
        
        if(gameState.isLose() or depth==0 or gameState.isWin()):
            curRes=self.evaluationFunction(gameState)
            return curRes
        actions=gameState.getLegalActions(0)
        v=-1000000000
        resAction=Directions.STOP
        res=-1000000000
        num=gameState.getNumAgents()
        curalpha=alpha
        for i in range(len(actions)):
                    newGameState=gameState.generateSuccessor(0, actions[i])
                    v=max(v, self.min_value(1, num, newGameState, depth, initialDepth, curalpha, beta))
                    if depth==initialDepth:
                        if v>res:
                            res=v
                            resAction=actions[i]
                    elif v>beta:
                        return v  
                    curalpha=max(curalpha, v)
        if depth==initialDepth:
            return resAction
        else:
            return v
        
        

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState, self.depth, self.depth, -10000000000, 10000000000) 

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    
    """ same method as in minimax"""
    def generateActions(self, gameState, ind, states, num):
        if(ind==num or gameState.isWin() or gameState.isLose()):
            states.append(gameState)
            return
        else:
            actions=gameState.getLegalActions(ind)
            for action in actions:
                newGameState=gameState.generateSuccessor(ind, action)
                self.generateActions(newGameState, ind+1, states, num)
        
        
        """ this method just returns the mean value for all his actions"""
    def exp_value(self, gameState, depth, initialDepth):
        if(gameState.isLose() or depth==0 or gameState.isWin()):
            curRes=self.evaluationFunction(gameState)
            return curRes
        states=[]
        num=gameState.getNumAgents()
        self.generateActions(gameState, 1, states, num)
        sum=0
        for state in states:
            sum+=self.max_value(state, depth-1, initialDepth)
        return float(sum)/len(states)
        
        
    """ same min_value method as in minimax above"""
    def max_value(self, gameState, depth, initialDepth):
        if(gameState.isLose() or depth==0 or gameState.isWin()):
            curRes=self.evaluationFunction(gameState)
            return curRes
        actions=gameState.getLegalActions(0)
        res=-100000;
        resAction='Center'
        for action in actions:
            newGameState=gameState.generateSuccessor(0, action)
            curRes=self.exp_value(newGameState, depth, initialDepth)
            if(curRes>res):
                resAction=action;
                res=curRes
        if depth==initialDepth:
            return resAction
        else:
            return res
        
        

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"      
        return self.max_value(gameState, self.depth, self.depth)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: as in the above evaluation function just measured minimal
                  distances to ghosts and food, number of left food and number of left capsules.
                  just took the linear combination of their inverses with coefficients: 10, -10, -2, 5
    """
    foods = currentGameState.getFood().asList()
    pacman = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostPositions()
    minFood = 1000000
    minGhost = 1000000
    res=currentGameState.getScore()
    capsulesNum = len(currentGameState.getCapsules())
    for food in foods:
        minFood = min(minFood, manhattanDistance(food, pacman))
    
    for ghost in ghosts:
        minGhost = min(minGhost, manhattanDistance(pacman, ghost))
    
    return res+(10.0/float(minFood+1))-(10.0/(minGhost+1))-2.0/(len(foods)+1)+5.0/(capsulesNum+1)
        

# Abbreviation
better = betterEvaluationFunction

