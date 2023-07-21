# A* Pathfinding visualization tool made for fun & learning purposes
# Currently following implementation and explanations by Tech With Tim to help create the core 
# source: https://www.youtube.com/watch?v=JtiK0DOeI4A

import pygame
from queue import PriorityQueue
import math

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# pygame init
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


class Node: 
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # to keep track of coordinate position
        self.x = row * width
        self.y = col * width
        # set default properties
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    # have already looked or considered this option
    def is_closed(self):
        return self.color == RED
    
    # open set or option
    def is_open(self):
        return self.color == GRAY
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == BLUE
    
    def is_end(self):
        return self.color == GREEN
    
    def reset(self):
        self.color == WHITE

    # to set everything
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GRAY
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = BLUE
    
    def make_end(self):
        self.color = GREEN

    def make_path(self):
        self.color = YELLOW

    # method called to draw cube on screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    # less than function to compare two Node objects together
    # similar to compareTo in Java
    def __lt__ (self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    # return absolute distance to find the L distance
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    # find width of each cube
    gap = width // rows

    # in grid row of i, append the spot (node) into it,
    # so the entire list/grid stores nodes
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            currNode = Node(i , j, gap, rows)
            grid[i].append(currNode)

    return grid


# make grid lines on pygame
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        # multiply curr index of row by gap
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows): 
            # flip coordinates to shift around the x axis to draw verticle lines
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)