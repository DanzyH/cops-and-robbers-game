import pygame
import sys
from button import Button
from util import *

class Start:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.background = pygame.image.load("assets/Background.png")
    
    def run(self):
        # Draw graphics
        self.display.blit(self.background, (0,0))

        mouse_pos = pygame.mouse.get_pos()

        menu_text = pygame.font.Font('assets/font.ttf', 100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(self.display.get_width() / 2, 100))
        self.display.blit(menu_text, menu_rect)

        PLAY_BUTTON = Button(image=None, pos=(self.display.get_width() / 2, 300), text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MAP_EDITOR_BUTTON = Button(image=None, pos=(self.display.get_width() / 2, 450), text_input="MAP EDITOR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(self.display.get_width() / 2, 600), text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        buttons = [
            PLAY_BUTTON, 
            MAP_EDITOR_BUTTON, 
            QUIT_BUTTON
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
                if PLAY_BUTTON.checkForInput(event.pos):
                    self.game_state_manager.setState('level_select')
                if MAP_EDITOR_BUTTON.checkForInput(event.pos):
                    self.game_state_manager.setState('edit')
                if QUIT_BUTTON.checkForInput(event.pos):
                    pygame.quit()
                    sys.exit()