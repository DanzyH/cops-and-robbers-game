import pygame
import sys
from button import Button
from util import *

class LevelSelector:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
    
    def run(self):
        # Draw graphics
        self.display.fill('red')

        mouse_pos = pygame.mouse.get_pos()

        start_btn = Button(image=None, pos=(self.display.get_width() / 2, 300), text_input="START", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        buttons = [
            start_btn
        ]

        for button in buttons:
            button.changeColor(mouse_pos)
            button.update(self.display)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.checkForInput(event.pos):
                    print('level play button pressed!')
                    self.game_state_manager.setState('play')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state_manager.setState('start')
        