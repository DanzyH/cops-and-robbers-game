class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def getState(self):
        return self.currentState
    
    def setState(self, state):
        self.currentState = state