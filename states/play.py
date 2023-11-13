import pygame
import sys

class Play():
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
    
    def run(self):
        # Draw graphics
        self.display.fill('blue')

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state_manager.setState('level_select')