"""
Class for maintaining explored sets
"""

class Explored(object):
    "Maintain an explored set."

    def __init__(self):
        "__init__() - Create an empty explored set"
        self.visited = set()


    def exists(self, state):
        """
        exists(state) - Has this state already been explored?
        :param state:  
        :return: True if already seen, False otherwise
        """
        return (state in self.visited)
        
        

    def add(self, state):
        """
        add(state) - Add a given state to the explored set
        :param state:  
        :return: None
        """
        self.visited.add(state)

