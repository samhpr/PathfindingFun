# A* Pathfinding visualization tool made for fun & learning purposes
# Currently following implementation and explanations by Tech With Tim to help create the core 
# source: https://www.youtube.com/watch?v=JtiK0DOeI4A
# more info: https://en.wikipedia.org/wiki/A*_search_algorithm


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
PURPLE = (138, 43, 226)

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
        return self.color == YELLOW
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == BLUE
    
    def is_end(self):
        return self.color == PURPLE
    
    def reset(self):
        self.color = WHITE

    # to set everything
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = YELLOW
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = BLUE
    
    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = GREEN

    # method called to draw cube on screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    ## updated for diagonal
    def update_neighbors(self, grid):
        self.neighbors = []
        # going DOWN
        if self.row < self.total_rows - 1:
            # going DOWN a row (checking if can move down)
            if not grid[self.row + 1][self.col].is_barrier(): 
                self.neighbors.append(grid[self.row + 1][self.col])

            # going DOWN and RIGHT
            if self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier(): 
                self.neighbors.append(grid[self.row + 1][self.col + 1])
            
            # going DOWN and LEFT
            if self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier(): 
                self.neighbors.append(grid[self.row + 1][self.col - 1])
            
        # going UP
        if self.row > 0:
            # going UP a row (checking if we can move up)
            if not grid[self.row - 1][self.col].is_barrier(): 
                self.neighbors.append(grid[self.row - 1][self.col])
            
            # going UP and RIGHT
            if self.col < self.total_rows - 1 and not grid[self.row- 1][self.col + 1].is_barrier():
                self.neighbors.append(grid[self.row - 1][self.col + 1])

            # going UP and LEFT
            if self.col > 0 and not grid[self.row- 1][self.col - 1].is_barrier():
                self.neighbors.append(grid[self.row - 1][self.col - 1])
        
        # GOING RIGHT
        if self.col < self.total_rows - 1:
            if not grid[self.row][self.col + 1].is_barrier():
                self.neighbors.append(grid[self.row][self.col + 1])

        # GOING LEFT
        if self.col > 0:
            if not grid[self.row][self.col - 1].is_barrier():
                self.neighbors.append(grid[self.row][self.col - 1])

    # similar to compareTo in Java
    def __lt__ (self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    # return absolute distance to find the L distance
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(is_from, currNode, draw):
    # traverse from start to the end and draw it
    while currNode in is_from:
        currNode = is_from[currNode]
        currNode.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    # 'push' is same as 'put'
    # we can use count to consider the tiebreakers (same F score)
    # .put('fscore', 'number', 'current node')

    # creating open set and put start node inside
    open_set.put((0, count, start))
    # keeps track of which nodes came from where to find best path at the end
    is_from = {}
    # keeps track of the shortest distance from the start node, to the current node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    # keeps track of the predicted distance from current node to the end node, following path with current node, what the distance will be to the end node
    f_score = {node: float("inf") for row in grid for node in row}
    # f score is the heuristic because we want to estimate how far end node is from the current node and give that a score
    f_score[start] = h(start.get_pos(), end.get_pos())

    # we want to make a set because the priority queue needs to be checked if there is something in it
    # aka, it keeps track of the items in the priority queue, and able to check
    open_set_hash = {start}

    # run until open set is empty, considered every possible node and path does not exist, or open set has nothing
    while not open_set.empty():
        for event in pygame.event.get():
            # feature to allow user to quit from while loop
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # start at 2 because we want to skip past start and end nodes
        # we can get the lowest number (current node) using priority queue as it keeps track the lowest number for example
        currNode = open_set.get()[2]
        # take whatever node from queue and ensure there are no duplicates by syncing with open set hash
        open_set_hash.remove(currNode)

        # say that if we are at the end, then we have finished
        if currNode == end:
            reconstruct_path(is_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        # otherwise consider all neighbors of current node
        for neighbor in currNode.neighbors:
            # calculate their tentative g score
            temp_g_score = g_score[currNode] + 1

            # if we found a better neighbor (g score) than the current, then we update values for better path
            if temp_g_score < g_score[neighbor]:
                is_from[neighbor] = currNode
                g_score[neighbor] = temp_g_score
                # find row column pos of the neighbor and add to f score with temp g score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                # add if not already in open set hash
                if neighbor not in open_set_hash:
                    # add to count to add it to the set, and then also put it into the set
                    count += 1
                    # add back into open set 
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        
        # if current is not the start node, then make it closed
        # so if the node we have already considered does not work, then close it
        if currNode != start:
            currNode.make_closed()

    # if we did not find a path       
    return False


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

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    # we are finding where the mouse in x and y, and dividing in by each position of 
    # the spot or cubes on the screen
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    
    return row, col
    

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    
    start = None
    end = None

    run = True

    # while this loop, go through all of the events that happened
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
            
            # check if pygame mouse is left mouse([0]) then do...
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()
            
            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # passing function that is equal to function call, Lamda is an anonymous function
                    # for example, x = Lamda: print("hello")
                    # calling x will call the print function
                    # essentially, a function without a name, more info: 
                    #           https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)