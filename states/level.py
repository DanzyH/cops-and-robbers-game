import pygame

class LevelSelector:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    
    def run(self):
        self.display.fill('red')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_2]:
            self.gameStateManager.setState('play')
        if keys[pygame.K_ESCAPE]:
            self.gameStateManager.setState('start')
        