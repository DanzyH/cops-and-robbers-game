import pygame
import sys
from const import *
from util import *
from button import Button

class Start:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.background = pygame.image.load("assets/Background.png")
        #self.background = '#DCDDD8'
    def run(self):
        # Draw graphics
        self.display.blit(self.background, (0,0))

        mouse_pos = pygame.mouse.get_pos()

        draw_text("MAIN MENU", get_font(FONT_PATH, 100), "#b68f40", SCREENWIDTH / 2, 100, "center", self.display)
        
        PLAY_BUTTON = Button(image=None, pos=(SCREENWIDTH / 2, 300), text_input="PLAY", font=get_font(FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")
        MAP_EDITOR_BUTTON = Button(image=None, pos=(SCREENWIDTH / 2, 450), text_input="MAP EDITOR", font=get_font(FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(SCREENWIDTH / 2, 600), text_input="QUIT", font=get_font(FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")

        buttons = [
            PLAY_BUTTON, 
            MAP_EDITOR_BUTTON, 
            QUIT_BUTTON
        ]

        for button in buttons:
            button.on_hover(mouse_pos)
            button.update(self.display)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(event.pos):
                    self.game_state_manager.setState('level_select')
                if MAP_EDITOR_BUTTON.check_for_input(event.pos):
                    self.game_state_manager.setState('edit')
                if QUIT_BUTTON.check_for_input(event.pos):
                    pygame.quit()
                    sys.exit()