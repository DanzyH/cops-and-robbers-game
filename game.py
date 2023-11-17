import pygame
from const import *
from gameState import GameStateManager
from states.start import Start
from states.editor import GraphEditor
from states.level import LevelSelector
from states.play import Play

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Cops and robbers")
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager("start")

        self.start = Start(self.screen, self.gameStateManager)
        self.editor = GraphEditor(self.screen, self.gameStateManager)
        self.levelSelector = LevelSelector(self.screen, self.gameStateManager)
        self.play = Play(self.screen, self.gameStateManager)

        self.states = {
            'start': self.start,
            'edit': self.editor,
            'level_select': self.levelSelector,
            'play': self.play 
            }
        
    def mainloop(self):
        while True:
            self.states[self.gameStateManager.get_state()].run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.mainloop()