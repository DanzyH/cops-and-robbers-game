import pygame
import sys
import os
import json
import math
from const import *
from tkinter import filedialog

CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Vertex class
class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.selected = False

    def draw(self, screen):
        color = RED if self.selected else BLACK
        borderColor = pygame.Color("Yellow")
        pygame.draw.circle(screen, borderColor, (self.x, self.y), self.radius + 5)
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

# Edge class
class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, screen):
        pygame.draw.line(screen, BLACK, (self.start.x, self.start.y), (self.end.x, self.end.y))

class GraphEditor:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.background = '#DCDDD8'
        self.vertices = []
        self.edges = []
        self.selected_vertex = None
        self.edge_start = None

    def save_graph(self):
        root = os.getcwd()
        file_path = filedialog.asksaveasfilename(initialdir=f"{root}/data/Custom levels/", title="Save Graph", filetypes=[("JSON files", "*.json")])
        data = {
            "vertices": [(vertex.x, vertex.y) for vertex in self.vertices],
            "edges": [(self.vertices.index(edge.start), self.vertices.index(edge.end)) for edge in self.edges]
        }
        with open(f"{file_path}.json", "w") as file:
            json.dump(data, file)

    def load_graph(self, file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                self.vertices = [Vertex(x, y) for x, y in data["vertices"]]
                self.edges = [Edge(self.vertices[start], self.vertices[end]) for start, end in data["edges"]]
        except FileNotFoundError:
            print(f"File '{file_path}'.json not found.")
    
    def load_file_dialog(self):
        root = os.getcwd()
        file_name = filedialog.askopenfilename(initialdir=f"{root}/data/Custom levels/", title="Select a graph file", filetypes=[("JSON files", "*.json")])
        return file_name
    
    def run(self):
        # Draw graphics
        if self.selected_vertex:
                x, y = pygame.mouse.get_pos()
                self.selected_vertex.x, self.selected_vertex.y = x, y
        self.display.fill(self.background)
        for edge in self.edges:
            edge.draw(self.display)
        for vertex in self.vertices:
            vertex.draw(self.display)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    for vertex in self.vertices:
                        distance = math.hypot(x - vertex.x, y - vertex.y)
                        if distance <= vertex.radius:
                            self.selected_vertex = vertex
                            self.selected_vertex.selected = True
                            self.edge_start = vertex
                            break
                    else:
                        new_vertex = Vertex(x, y)
                        self.vertices.append(new_vertex)
                if event.button == 3:  # Right mouse button
                    x, y = event.pos
                    for vertex in self.vertices:
                        distance = math.hypot(x - vertex.x, y - vertex.y)
                        if distance <= vertex.radius:
                            if self.edge_start is not None and self.edge_start != vertex:
                                self.edges.append(Edge(self.edge_start, vertex))
                                self.edge_start = None
                            break
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    if self.selected_vertex:
                        self.selected_vertex.selected = False
                        self.selected_vertex = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE and self.selected_vertex:
                    self.vertices.remove(self.selected_vertex)
                    self.edges = [edge for edge in self.edges if edge.start != self.selected_vertex and edge.end != self.selected_vertex]
                    self.selected_vertex = None
                    self.edge_start = None
                if event.key == pygame.K_s:
                    self.save_graph()

                if event.key == pygame.K_l:
                    file_path = self.load_file_dialog()
                    if file_path:
                        self.load_graph(file_path)
                if event.key == pygame.K_ESCAPE:
                    self.running = False