import pygame
import sys
from gameState import GameStateManager
from states.level import LevelSelector
from states.start import Start
from states.play import Play

SCREENWIDTH, SCREENHEIGHT = 1280, 700
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Cops and robbers")
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager("start")

        self.start = Start(self.screen, self.gameStateManager)
        self.levelSelector = LevelSelector(self.screen, self.gameStateManager)
        self.play = Play(self.screen, self.gameStateManager)

        self.states = {
            'start': self.start, 
            'play': self.play, 
            'level_select': self.levelSelector
            }
        
    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.states[self.gameStateManager.getState()].run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.mainloop()