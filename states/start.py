import pygame

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    
    def run(self):
        self.display.fill('green')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.gameStateManager.setState('level_select')