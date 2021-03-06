# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys

from game import Agent

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
        if (action == Directions.STOP):
            return -1000000
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newFoodList = newFood.asList()
        for c in successorGameState.getCapsules():
            newFoodList.append(c)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        fDist = 100000
        gDist = 100000
        newGhostPositions = successorGameState.getGhostPositions()
        for gPos in newGhostPositions:
            gD = manhattanDistance(newPos, gPos);
            if (gD <= gDist):
                gDist = gD
        for foodLoc in newFoodList:
            d = manhattanDistance(newPos, foodLoc)
            if (d <= fDist):
                fDist = d
        return 1.0 / fDist - (1.0 / (0.01 + gDist)) + min(newScaredTimes) + successorGameState.getScore()

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
        move = self.minimax(gameState, self.depth, self.index)
        return move[0]

    def minimax(self, gameState, depth, agentIndex):
        legalMoves = gameState.getLegalActions(agentIndex)
        if (depth == 0 or legalMoves == []):
            return ("Leaf", self.evaluationFunction(gameState))
        if (agentIndex == 0):
            bestMove = ("Nothing", -(sys.maxint - 1))
            for move in legalMoves:
                successorState = gameState.generateSuccessor(agentIndex, move)
                val = self.minimax(successorState, depth, agentIndex + 1)
                if (val[1] > bestMove[1]):
                    bestMove = (move, val[1])
            return bestMove
        elif (agentIndex < gameState.getNumAgents()):
            bestMove = ("Nothing", sys.maxint)
            for move in legalMoves:
                successorState = gameState.generateSuccessor(agentIndex, move)
                if (agentIndex + 1 >= gameState.getNumAgents()):
                    val = self.minimax(successorState, depth - 1, 0)
                else:
                    val = self.minimax(successorState, depth, agentIndex + 1)
                if (val[1] < bestMove[1]):
                    bestMove = (move, val[1])
            return bestMove
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = -sys.maxint -1
        beta = sys.maxint
        move = self.minimax(gameState, self.depth, self.index, alpha, beta)
        return move[0]

    def minimax(self, gameState, depth, agentIndex, alpha, beta):
        legalMoves = gameState.getLegalActions(agentIndex)
        if (depth == 0 or legalMoves == []):
            return ("Leaf", self.evaluationFunction(gameState))
        if (agentIndex == 0):
            bestMove = ("Nothing", -(sys.maxint - 1))
            for move in legalMoves:
                successorState = gameState.generateSuccessor(agentIndex, move)
                val = self.minimax(successorState, depth, agentIndex + 1, alpha, beta)
                if (val[1] > bestMove[1]):
                    bestMove = (move, val[1])
                if (val[1] > beta):
                    return bestMove
                alpha = max(alpha, val[1])
            return bestMove
        elif (agentIndex < gameState.getNumAgents()):
            bestMove = ("Nothing", sys.maxint)
            for move in legalMoves:
                successorState = gameState.generateSuccessor(agentIndex, move)
                if (agentIndex + 1 >= gameState.getNumAgents()):
                    val = self.minimax(successorState, depth - 1, 0, alpha, beta)
                else:
                    val = self.minimax(successorState, depth, agentIndex + 1, alpha, beta)
                if (val[1] < bestMove[1]):
                    bestMove = (move, val[1])
                if (val[1] < alpha):
                    return bestMove
                beta = min(beta, val[1])
            return bestMove
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        move = self.expectimax(gameState, self.depth, self.index)
        return move[0]

    def expectimax(self, gameState, depth, agentIndex):
        legalMoves = gameState.getLegalActions(agentIndex)
        if (depth == 0 or legalMoves == []):
            return ("Leaf", self.evaluationFunction(gameState))
        if (agentIndex == 0):
            bestMove = ("Nothing", (-sys.maxint -1) * 1.0)
            for move in legalMoves:
                successorState = gameState.generateSuccessor(agentIndex, move)
                val = self.expectimax(successorState, depth, agentIndex + 1)
                if (val[1] > bestMove[1]):
                    bestMove = (move, val[1])
            return bestMove
        elif (agentIndex < gameState.getNumAgents()):
            bestMove = ("Nothing", 0.0)
            for move in legalMoves:
                successorState = gameState.generateSuccessor(agentIndex, move)
                if (agentIndex + 1 >= gameState.getNumAgents()):
                    val = self.expectimax(successorState, depth - 1, 0)
                else:
                    val = self.expectimax(successorState, depth, agentIndex + 1)
                p = 1.0 / (len(legalMoves) * 1.0)
                bestMove = (bestMove[0], bestMove[1] + (p * val[1]))
            return bestMove
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    # Check if game is over
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return -float("inf")
    
    score = scoreEvaluationFunction(currentGameState)
    foodGrid = currentGameState.getFood()
    foodList = foodGrid.asList()
    ghostList = currentGameState.getGhostPositions()
    foodDist = float("inf")
    ghostDist = float("inf")
    pacPos = currentGameState.getPacmanPosition()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    scaredSum = 0;

    # Get sum of scared times
    for sTime in scaredTimes:
        scaredSum += sTime

    # Get manhattan distace between pacman and each food pellet. Keep smallest distance.
    for food in foodList:
        fD = manhattanDistance(pacPos, food)
        if (fD < foodDist):
            foodDist = fD

    # Get manhattan distace between pacman and each ghost. Keep smallest distance.
    for ghost in ghostList:
        gD = manhattanDistance(pacPos, ghost)
        if (gD < ghostDist):
            ghostDist = gD

    # Assign scores with the values calculated above multiplied by arbitrary weights.
    score += max(ghostDist, 4) * 2
    score -= foodDist * 2.5
    score -= 4 * len(foodList)

    if (scaredSum == 0):
        score -= 3.5 * len(capsules)
    else:
        score += scaredSum

    return score
        
# Abbreviation
better = betterEvaluationFunction

