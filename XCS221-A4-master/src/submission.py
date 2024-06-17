from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
# BEGIN_HIDE
# END_HIDE

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument
    is an object of GameState class. Following are a few of the helper methods that you
    can use to query a GameState object to gather information about the present state
    of Pac-Man, the ghosts and the maze.

    gameState.getLegalActions():
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action):
        Returns the successor state after the specified agent takes the action.
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    gameState.getScore():
        Returns the score corresponding to the current state of the game


    The GameState class is defined in pacman.py and you might want to look into that for
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    # BEGIN_HIDE
    # END_HIDE

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # BEGIN_HIDE
    # END_HIDE
    return successorGameState.getScore()


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

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following:
      pacman won, pacman lost or there are no legal moves.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.getScore():
        Returns the score corresponding to the current state of the game

      gameState.isWin():
        Returns True if it's a winning state

      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue

    """
    pass
    # ### START CODE HERE ###
    depth_level = self.depth
    startAgentIndex = 0

    def recurse(gameState, agentIndex, depth_level):
      if_win = gameState.isWin()
      if_lose = gameState.isLose()
      curr_score = gameState.getScore()
      if if_win or if_lose:
        return (curr_score, Directions.STOP)
      elif depth_level == 0:
        eval = self.evaluationFunction(gameState)
        return (eval, Directions.STOP)
      else:
        ghost_num = gameState.getNumAgents()
        newIndex = agentIndex + 1
        if newIndex == ghost_num:
          newIndex = 0
          depth_level -= 1

        choices = [(recurse(gameState.generateSuccessor(agentIndex, action), newIndex, depth_level)[0], action) for action in gameState.getLegalActions(agentIndex)]
        if agentIndex == 0:
          return max(choices)
        else:
          return min(choices)

    value, action = recurse(gameState, startAgentIndex, depth_level)
    return action
    # ### END CODE HERE ###

######################################################################################
# Problem 2a: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    pass
    # ### START CODE HERE ###
    depth_level = self.depth
    startAgentIndex = 0
    startAlpha = float('-inf')
    startBeta = float('inf')

    def recurse(gameState, agentIndex, depth_level, alpha, beta):
      if_win = gameState.isWin()
      if_lose = gameState.isLose()
      curr_score = gameState.getScore()
      if if_win or if_lose:
        return (curr_score, Directions.STOP)
      elif depth_level == 0:
        eval = self.evaluationFunction(gameState)
        return (eval, Directions.STOP)
      else:
        ghost_num = gameState.getNumAgents()
        newIndex = agentIndex + 1
        the_action = 'num'
        if newIndex == ghost_num:
          newIndex = 0
          depth_level -= 1
        if agentIndex == 0:
          for action in gameState.getLegalActions(agentIndex):
            score = recurse(gameState.generateSuccessor(agentIndex, action), newIndex, depth_level, alpha, beta)[0]
            if score > alpha:
              the_action = action
            alpha = max(alpha, score)
            if alpha > beta:
              break
          return alpha, the_action
        else:
          for action in gameState.getLegalActions(agentIndex):
            score = recurse(gameState.generateSuccessor(agentIndex, action), newIndex, depth_level, alpha, beta)[0]
            if score > beta:
              the_action = action
            beta = min(beta, score)
            if alpha > beta:
              break
          return beta, the_action

    value, action = recurse(gameState, startAgentIndex, depth_level, startAlpha, startBeta)
    return action
    # ### END CODE HERE ###

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    pass
    # ### START CODE HERE ###
    depth_level = self.depth
    startAgentIndex = 0

    def recurse(gameState, agentIndex, depth_level):
      if_win = gameState.isWin()
      if_lose = gameState.isLose()
      curr_score = gameState.getScore()
      if if_win or if_lose:
        return (curr_score, Directions.STOP)
      elif depth_level == 0:
        eval = self.evaluationFunction(gameState)
        return (eval, Directions.STOP)
      else:
        ghost_num = gameState.getNumAgents()
        newIndex = agentIndex + 1
        if newIndex == ghost_num:
          newIndex = 0
          depth_level -= 1

        choices = [(recurse(gameState.generateSuccessor(agentIndex, action), newIndex, depth_level)[0], action) for
                   action in gameState.getLegalActions(agentIndex)]
        if agentIndex == 0:
          return max(choices)
        else:
          summation = 0
          for choice in choices:
            summation += choice[0]
          return (summation / len(choices), random.choice(gameState.getLegalActions(agentIndex)))

    value, action = recurse(gameState, startAgentIndex, depth_level)
    return action
    # ### END CODE HERE ###

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
    To calculate my score I used the current score, the distance to the closest food, and number of food pieces left.

  """
  pass
  # ### START CODE HERE ###
  # The code below is when ther is a lose or win situation, in which the return is either infinity or negative inf
  if currentGameState.isLose():
    return -float("inf")
  elif currentGameState.isWin():
    return float("inf")
  #I need the current position of the pacman which I do below:
  position = currentGameState.getPacmacPosition()
  # I am using the mnahttan distance function between our position and the food by getting the food list, and using
  # a lambda function with the manhattan distance function to find the closest food
  foods = currentGameState.getFood().asList()
  closestfooddistance = min(map(lambda x: util.manhattanDistance(position, x), foods))
  # Use foods and find the length to get the number of food pieces there are left
  numfoodleft = len(foods)
  # Now I will calculate the current score based on the scoreEvaluationFunction
  currentscore = scoreEvaluationFunction(currentGameState)
  # Calcution of the final outputted score
  score = 1 * currentscore + -1.5 * closestfooddistance + -4 * numfoodleft

  return score

  # ### END CODE HERE ###

# Abbreviation
better = betterEvaluationFunction
