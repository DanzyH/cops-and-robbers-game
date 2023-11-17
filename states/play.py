import pygame
import sys
import os
import json
import networkx as nx
import random
from button import Button
from const import *
from util import *
import random

root = os.getcwd()

class Node:
    def __init__(self, pos, img):
        self.x = pos[0]
        self.y = pos[1]
        self.img = pygame.image.load(img).convert_alpha()
        self.rect = self.img.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.img, self.rect)

class Play():
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.background = '#DCDDD8'
        self.game_data = None
        self.graph = nx.Graph()
        self.nodes = []
        self.cop_node = None
        self.robber_node = None
        self.is_robber_turn = True
        self.turn = 0
    
    def load_game_data(self):
        if self.game_data is None:
            with open(f"{root}/data/{GAME_DATA_FILE}", 'r') as openfile:
                # Reading from json file
                self.game_data = json.load(openfile)
                # Load nodes data
                for index, node_data in enumerate(self.game_data["vertices"]):
                    self.graph.add_node(index, pos=node_data, img=f"{root}/assets/location_{random.randint(1, 12)}.png")
                    self.nodes.append(Node(self.graph.nodes[index]["pos"], self.graph.nodes[index]["img"]))
                # Load edges data
                for edge_data in self.game_data["edges"]:
                    self.graph.add_edge(edge_data[0], edge_data[1])
            self.restart()
            
    def switch_turn(self):
        self.is_robber_turn = not self.is_robber_turn
    
    def evaluation_function(self, chaser_position_index, target_position_index):
        if chaser_position_index == target_position_index:
            return float('inf')  # Maximum score if the target player is caught

        distance = nx.shortest_path_length(self.graph, source=chaser_position_index, target=target_position_index)

        # The closer the chasing player is to the target player, the higher the score
        score = 1 / (distance + 1)

        return score
    
    def chase_algorithm(self, chaser_position_index, target_position_index):
        neighbors = list(self.graph.neighbors(chaser_position_index))

        best_move = None
        best_score = float('-inf')

        for neighbor in neighbors:
            score = self.evaluation_function(neighbor, target_position_index)

            if score > best_score:
                best_score = score
                best_move = neighbor

        return best_move

    def ai_move(self):
        self.cop_node = self.chase_algorithm(self.cop_node, self.robber_node)
        self.switch_turn()

    def player_move(self, destination_index, is_robber):
        if is_robber: 
            self.robber_node = destination_index
            self.turn += 1
        else: self.cop_node = destination_index
        self.switch_turn()

    def check_game_over(self):
        return self.cop_node == self.robber_node or self.turn > len(self.graph.edges) + 1

    def reset(self):
        self.game_data = None
        self.graph.clear()
        self.nodes.clear()
        self.is_robber_turn = True
        self.turn = 0

    def restart(self):
        self.cop_node = random.randint(0, len(self.graph.nodes) - 1)
        while True:
            self.robber_node = random.randint(0, len(self.graph.nodes) - 1)
            if self.robber_node != self.cop_node:
                break
        self.is_robber_turn = True
        self.turn = 0

    def draw_edge(self, edge):
        start_pos = self.graph.nodes[edge[0]]["pos"]
        end_pos = self.graph.nodes[edge[1]]["pos"]
        pygame.draw.line(self.display, "#232227", start_pos, end_pos, 3)

    def draw_player(self, pos, img):
        player_img = pygame.image.load(img).convert_alpha()
        player_rect = player_img.get_rect(center=pos)
        self.display.blit(player_img, player_rect)

    def run(self):
        # Load game data
        self.load_game_data()

        # Draw graphics
        self.display.fill(self.background)
        draw_text(f"{'Robber' if self.is_robber_turn else 'Cop'}'s turn", get_font(FONT_PATH, 25), '#232227', 10, 25, 'left', self.display)
        draw_text(f"{len(self.graph.edges) + 2 - self.turn} until the robber escape", get_font(FONT_PATH, 25), '#232227', 10, 50, 'left', self.display)

        MENU_BUTTON = Button(image=None, pos=(SCREENWIDTH * 3 / 4 + 200, 25), text_input="Menu", font=get_font(FONT_PATH, 25), base_color="#232227", hovering_color="red")

        buttons = [
            MENU_BUTTON,
        ]

        for button in buttons:
            button.on_hover(pygame.mouse.get_pos())
            button.update(self.display)

        # Draw edges
        for edge in self.graph.edges():
            self.draw_edge(edge)
            #print(edge)

        # Draw nodes
        for node in self.nodes:
           pygame.draw.circle(self.display, self.background, (node.x, node.y), 25)
           node.draw(self.display)

        # Draw players
        cop_postion = self.graph.nodes[self.cop_node]["pos"]
        robber_postion = self.graph.nodes[self.robber_node]["pos"]
        self.draw_player((cop_postion[0] + 25, cop_postion[1] + 25), f"{root}/assets/Cop.png")
        self.draw_player((robber_postion[0] + 25, robber_postion[1] + 25), f"{root}/assets/Robber.png")
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button clicked
                    if MENU_BUTTON.check_for_input(event.pos):
                        self.reset()
                        self.game_state_manager.set_state('start')
                    for i in range(len(self.nodes)):
                        if self.nodes[i].rect.collidepoint(event.pos): # Node clicked
                            #print(self.graph.nodes[i])
                            if i in list(self.graph.neighbors(self.robber_node if self.is_robber_turn else self.cop_node)):
                                #print(f"{self.graph.nodes[i]}, True")
                                self.player_move(i, self.is_robber_turn)
                                if not self.is_robber_turn and self.game_data["game_mode"] == "PVE":
                                    self.ai_move()
                    if self.check_game_over():
                        print(f"Game over! {'Robber' if self.turn > len(self.graph.edges) + 1 else 'Cop'} win last game.")
                        self.restart()
                
                        
                    