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


from ast import Num
from dis import dis
from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent
from pacman import GameState


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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

        # def getManhattenDistance(StartState:Any,Goal:Any):
        #     xy1 = StartState
        #     xy2 = Goal
        #     return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostPos = [ghostState.getPosition()
                       for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        def getManhattenDistance(StartState, Goal):
            xy1 = StartState
            xy2 = Goal
            return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

        foodEaten = newPos in currentGameState.getFood().asList()

        if successorGameState.isWin():
            return successorGameState.getScore()
        elif successorGameState.isLose():
            return -999999 + successorGameState.getScore()

        # # Add awareness of ghost distance
        for posGhost in newGhostPos:
            if posGhost == newPos:
                return 0
        # foodList = newFood.asList()
        # print(newFood.asList())
        # if newPos in foodList:
        #     print('Eat')
        #     return 999999

        minDistance = 9999999
        for food in newFood.asList():
            if(foodEaten):
                return 999999
            distance = getManhattenDistance(newPos, food)
            if distance < minDistance:
                minDistance = distance
        # print(currentGameState.getPacmanState())
        #print('%s %x',newPos,1/minDistance)
        return 1/minDistance


def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        def inner(currState, index, depth):
            print("index:", index, "depth:", depth)
            if depth == 0:
                return self.evaluationFunction(currState)
            actions = currState.getLegalActions(index)
            optimal_value = 999999
            if index == 0:
                optimal_value = -999999
            for action in actions:
                newState = currState.generateSuccessor(index, action)
                if newState.isWin() or newState.isLose():
                    value = self.evaluationFunction(newState)
                else:
                    if index == gameState.getNumAgents() - 1:
                        new_depth = depth - 1
                        new_index = 0
                    else:
                        new_depth = depth
                        new_index = index + 1
                    value = inner(newState, new_index, new_depth)
                if index == 0:
                    optimal_value = max(optimal_value, value)
                else:
                    optimal_value = min(optimal_value, value)
            return optimal_value

        optimal = None
        max_value = -999999
        pacActions = gameState.getLegalActions(0)
        for action in pacActions:
            newState = gameState.generateSuccessor(0, action)
            if newState.isWin() or newState.isLose():
                value = self.evaluationFunction(newState)
            else:
                value = inner(newState, 1, self.depth)
            if value >= max_value:
                max_value = value
                optimal = action
        return optimal


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
