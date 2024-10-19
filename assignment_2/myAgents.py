from pacman import Directions, GameState
from game import Agent, Actions, AgentState
from pacmanAgents import LeftTurnAgent

class TimidAgent(Agent):
    """
    A simple agent for PacMan
    """
    def __init__(self):
        super().__init__()  # Call parent constructor
        # Add anything else you think you need here
    
    # returns direction to go in
    def getAction(self, state):
        """
        getAction(state) - Make a decsion based on the current game state
        state - pacman.GameState instance
        returns a valid action direction:  North, East, South, West or
        a Stop action when no legal actions are possible
        """
        # get agent states
        pacmanState = state.getPacmanState()
        ghostStates = state.getGhostStates()
        
        # get legal moves for this instance
        legal = state.getLegalPacmanActions()
        
        # for each ghost, check if pacman is in danger, if so, evade
        for x in ghostStates:
            dangerDirection = self.inDanger(pacmanState, x)
            if (dangerDirection != Directions.STOP):
                return self.evadeGhost(dangerDirection, legal)
        
        # if no danger, do LeftTurnAgent
        return LeftTurnAgent.getAction(self, state)
    
    # if in danger, return which direction danger is in
    def inDanger(self, pacmanState, ghostState, dist=3):
        """
        inDanger(pacman, ghost) - Is the pacman in danger
        For better or worse, our definition of danger is when the pacman and
        the specified ghost are:
           in the same row or column,
           the ghost is not scared,
           and the agents are <= dist units away from one another

        If the pacman is not in danger, we return Directions.STOP
        If the pacman is in danger we return the direction to the ghost.
        """
        # getting nessesary state attributes
        pacman = pacmanState.getPosition()
        ghost = ghostState.getPosition()
        ghostScared = AgentState.isScared(ghostState)
        
        # ghosts who are scared pose no threat, continue as normal
        if (ghostScared):
            return Directions.STOP
        
        # checks if in same row, then dist (+ difference is west, - difference is east)
        # checks if in same col, then dist (+ difference is south, - difference is north)
        if ((pacman[1] == ghost[1]) & (abs(pacman[0] - ghost[0]) <= dist)):
            if((pacman[0] - ghost[0]) > 0):
                return Directions.WEST
            elif((pacman[0] - ghost[0]) < 0):
                return Directions.EAST
        elif((pacman[0] == ghost[0]) & (abs(ghost[1] - pacman[1]) <= dist)):
            if((pacman[1] - ghost[1]) > 0):
                return Directions.SOUTH
            elif((pacman[1] - ghost[1]) < 0):
                return Directions.NORTH
        
        # if not nearby, no nessesary action needed
        return Directions.STOP
    
    # my own function, to simplify the evading process
    # first try backwards, then as follows: left, right, forward
    # directions are in reference to ghost
    def evadeGhost(self, danger, legal):
        # directions are in reference to ghost
        left = Directions.LEFT[danger]  # What is left based on danger direction
        right = Directions.RIGHT[danger]
        reverse = Directions.REVERSE[danger]
        forward = danger
        
        if reverse in legal:
            action = reverse # run away
        else:
            # No running away
            if left in legal:
                action = left  # Turn left
            elif right in legal:
                action = right  # Turn right
            elif forward in legal:
                action = forward  # Towards the danger we go
            else:
                action = Directions.STOP  # Can't move!

        return action
