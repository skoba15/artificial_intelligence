# search.py
# ---------
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
from sre_constants import SUCCESS


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    
    """ closed -- list which keeps visited states in it
        fringe -- Fringe in this case is Stack. I keep lists in it, which include
                    tuples of state, direction and cost. Therefore each list
                    is a representation of a path from the start to the last state
        Algorithm --  on each iteration I take a list from the fringe and the last 
                    tuple from it(which is indeed the last visited state). Then I use
                    that state to get its neighbours and add to the fringe. the process
                    is terminated as soon as the popped state turns out to be 
                    a goal state, then I just iterate over the list and add the directions
                    to the result list"""
    from util import Stack
    closed=[]
    fringe = Stack() 
    initialList=[]
    startState = (problem.getStartState(), "-", 0)
    initialList.append(startState)
    fringe.push(initialList)
    while (1):
        if fringe.isEmpty(): return []
        node = fringe.pop()
        curState = node[len(node)-1][0]
        if problem.isGoalState(curState):
            return getList(node)
        if curState not in closed:
            closed.append(curState)
            successors=problem.getSuccessors(curState)
            for adjacent in successors:
                lst=list(node)
                lst.append(adjacent)
                fringe.push(lst)
    



""" iterates over a list of some states and adds the directions to the result list"""
def getList(lst):
    result=[]
    for i in range(1, len(lst)):
        result.append(lst[i][1])
    return result

    
""" the description is the same as for dfs, the minor change is in the fringe which is 
    now a queue"""
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue
    closed=[]
    fringe = Queue()
    initialList=[]
    startState = (problem.getStartState(), "-", 0)
    initialList.append(startState)
    fringe.push(initialList)
    while (1):
        if fringe.isEmpty(): return []
        node = fringe.pop()
        curState = node[len(node)-1][0]
        if problem.isGoalState(curState):
            return getList(node)
        if curState not in closed:
            closed.append(curState)
            successors=problem.getSuccessors(curState)
            for adjacent in successors:
                lst=list(node)
                lst.append(adjacent)
                fringe.push(lst)


""" the description is almost the same as for bfs, In this case I use PriorityQueue because
    the graph is weighted, therefore each state transition has different cost. In this case Priority Queue
    pops the path with the lowest cost"""
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from util import PriorityQueue
    closed=[]
    fringe = PriorityQueue()
    initialList=[]
    startState = (problem.getStartState(), "-", 0)
    initialList.append(startState)
    fringe.push(initialList, 0)
    while (1):
        if fringe.isEmpty(): return []
        node = fringe.pop()
        curState = node[len(node)-1][0]
        if problem.isGoalState(curState):
            return getList(node)
        if curState not in closed:
            closed.append(curState)
            successors=problem.getSuccessors(curState)
            for adjacent in successors:
                lst=list(node)
                lst.append(adjacent)
                fringe.push(lst,getListCost(lst)+adjacent[2])
                

"""returns the cost of the path, by iterating over the state transition prices and summing them """                
def getListCost(lst):
    cost=0;
    for i in range(1, len(lst)):
        cost=cost+lst[i][2]
    return cost
                
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


"""almost the same as UCS, in this case each state has an heuristic additionally, 
    and the price from startstate to the current state happens to be the sum of the real distance
    and heuristic in this state"""
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    closed=[]
    fringe = PriorityQueue()
    initialList=[]
    startState = (problem.getStartState(), "-", 0)
    initialList.append(startState)
    fringe.push(initialList, heuristic(problem.getStartState(), problem))
    while (1):
        if fringe.isEmpty(): return []
        node = fringe.pop()
        curState = node[len(node)-1][0]
        if problem.isGoalState(curState):
            return getList(node)
        if curState not in closed:
            closed.append(curState)
            successors=problem.getSuccessors(curState)
            for adjacent in successors:
                lst=list(node)
                lst.append(adjacent)
                fringe.push(lst,getListCost(lst)+heuristic(adjacent[0], problem))
            


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
