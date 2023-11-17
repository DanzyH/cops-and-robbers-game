import pygame
import sys
import os
import json
from const import *
from button import Button
from util import *

GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

TAB_MARGIN = 10
TAB_WIDTH, TAB_HEIGHT = 200, 30
ITEM_WIDTH, ITEM_HEIGHT = TAB_WIDTH * 2 + TAB_MARGIN, 40

root = os.getcwd()

def get_json_file_names(folder_path):
    json_files = [f[:-5] for f in os.listdir(folder_path) if f.endswith('.json')]
    return json_files

class LevelSelector:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        
        # Graphics attributes
        self.background = '#DCDDD8'

        self.list_offset = 0
        self.visible_items = 12
        
        # public_levels || custom_levels
        self.tabs = {
            'Public levels': get_json_file_names(f"{root}/data/Public levels/"),
            'Custom levels': get_json_file_names(f"{root}/data/Custom levels/")
        } 
        self.current_tab = list(self.tabs.keys())[0]
        
        # Game data attributes
        self.selected_level = None
        self.game_mode = "PVP"
    
    def reset(self):
        self.list_offset = 0
        self.current_tab = list(self.tabs.keys())[0]
        self.game_mode = "PVP"
        self.selected_level = None

    def run(self):
        # Draw graphics
        self.display.fill(self.background)
        mouse_pos = pygame.mouse.get_pos()

        draw_text("SELECT LEVEL", get_font(FONT_PATH, 100), "#b68f40", SCREENWIDTH / 2, 100, "center", self.display)

        # Draw level select section background
        level_list_rect = pygame.Rect(10, 200, self.display.get_width() // 2 - 10, ITEM_HEIGHT * self.visible_items)
        pygame.draw.rect(self.display, GRAY, level_list_rect)

        # Draw tabs
        tab_x = TAB_MARGIN
        for tab_name in self.tabs.keys():
            tab_rect = pygame.Rect(tab_x, level_list_rect[1] - TAB_HEIGHT, TAB_WIDTH, TAB_HEIGHT)
            pygame.draw.rect(self.display, GRAY if tab_name == self.current_tab else WHITE, tab_rect)
            pygame.draw.rect(self.display, BLACK, tab_rect, 2)

            # Display tab text
            draw_text(tab_name, get_font(None, 24), BLACK, tab_rect.left + 10, tab_rect.top + TAB_HEIGHT // 2, "left", self.display)
            tab_x += TAB_WIDTH + TAB_MARGIN

        # Draw items for the current tab
        item_data = self.tabs[self.current_tab]
        for i in range(self.list_offset, self.list_offset + self.visible_items):
            if 0 <= i < len(item_data):
                item_rect = (level_list_rect[0], level_list_rect[1] + (i - self.list_offset) * ITEM_HEIGHT, level_list_rect[2], ITEM_HEIGHT)
                draw_text(item_data[i], get_font(None, 36), BLACK, item_rect[0] + 10, item_rect[1] + ITEM_HEIGHT // 2, 'left', self.display)

                # Highlight the clicked item
                if is_point_inside_rect(mouse_pos, item_rect) or item_data[i] == self.selected_level:
                    pygame.draw.rect(self.display, (150, 150, 150), item_rect, 2)
        
        START_BTN = Button(image=None, pos=(SCREENWIDTH * 3 / 4, 300), text_input="START", font=get_font(FONT_PATH, 75), base_color="#232227", hovering_color="red")
        GAME_MODE_BTN = Button(image=None, pos=(SCREENWIDTH * 3 / 4, 450), text_input=f"<{self.game_mode}>", font=get_font(FONT_PATH, 75), base_color="#232227", hovering_color="red")
        BACK_BUTTON = Button(image=None, pos=(SCREENWIDTH * 3 / 4, 600), text_input="BACK", font=get_font(FONT_PATH, 75), base_color="#232227", hovering_color="red")
             
        buttons = [
            START_BTN,
            GAME_MODE_BTN,
            BACK_BUTTON
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
                if event.button == 4:  # Scroll up
                    if (self.visible_items < len(item_data)):
                        self.list_offset = max(0, self.list_offset - 1)
                elif event.button == 5:  # Scroll down
                    if (self.visible_items < len(item_data)):
                        self.list_offset = min(len(item_data) - self.visible_items, self.list_offset + 1)
                elif event.button == 1:  # Left mouse button click
                    
                    # Check if a button was clicked
                    if START_BTN.check_for_input(event.pos):
                        if self.selected_level:
                            folder_path = f"{root}/data/{self.current_tab}"
                            with open(f"{folder_path}/{self.selected_level}.json", 'r') as openfile:
                                # Reading from json file
                                json_data = json.load(openfile)
                            json_data['game_mode'] = self.game_mode
                            with open(f"{root}/data/{GAME_DATA_FILE}", 'w') as outfile:
                                # Writing to json file
                                json.dump(json_data, outfile)
                            print(json_data['game_mode'])
                            self.reset()
                            self.game_state_manager.set_state('play')
                    if BACK_BUTTON.check_for_input(event.pos):
                        self.reset()
                        self.game_state_manager.set_state('start')
                    if GAME_MODE_BTN.check_for_input(event.pos):
                        if self.game_mode == 'PVP':
                            self.game_mode = 'PVE'
                        else:
                            self.game_mode = 'PVP'
                    
                    # Check if a tab was clicked
                    tab_x = TAB_MARGIN
                    for tab_name in self.tabs.keys():
                        tab_rect = pygame.Rect(tab_x, level_list_rect[1] - TAB_HEIGHT, TAB_WIDTH, TAB_HEIGHT)
                        if tab_rect.collidepoint(event.pos):
                            self.current_tab = tab_name
                            print(f"Tab clicked: {self.current_tab}")
                            self.selected_level = None
                            self.list_offset = 0
                            break
                        tab_x += TAB_WIDTH + TAB_MARGIN
                    
                    # Item list clicked
                    if is_point_inside_rect(event.pos, level_list_rect):
                        clicked_item_index = (event.pos[1] - level_list_rect[1]) // ITEM_HEIGHT + self.list_offset
                        if 0 <= clicked_item_index < len(item_data):
                            self.selected_level = item_data[clicked_item_index]
                            print(f"Level Clicked: {self.selected_level}")