import pygame
import copy

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GOLD    = (255,215,0)
COLORS  = [(255,0,0,80),    # Red
          (255,165,0,80),  # Orange
          (255,255,0,80),  # Yellow
          (0,255,0,80),    # Green
          (255,0,255,80),  # Magenta
          (0,0,255,80),    # Blue
          (128,0,128,80)]  # Purple
VISITED = (0,0,255,60)
class Node():
    def __init__(self, position, child = None):
        self.position = position
        self.child = child
        self.pathCost = 0
        if child is not None:
            self.pathCost = child.pathCost + 1
            
    def __eq__(self, other):
        return self.position == other.position          

class Map():
    '''
        dimensions -> [x, y] as a list containing the width (x) and the height (y) of the map.
        robots     -> [Node(), Node()] as a list of Nodes representing the paths for each of the  
                      robots in the map.
        goal       -> [x, y] as a list containing the coordinate pair representing the goal 
                      location.
        map        -> [[]] as the two dimensional list containing map information. 
                      if map[x][y] == 1: map[x][y] contains an obstruction.
                      if map[x][y] == 0: map[x][y] is a free space. 
        offsetX    -> Integer representing the square offset for the X coordinate when displaying the map.
        offsetY    -> Integer representing the square offset for the Y coordinate when displaying the map.
        visited    -> [(x, y)] list containing coordinate tuples of all points visited by robot 0.
    '''
    def __init__(self, file):
        # read in map data from file
        self.dimensions = [int(i) for i in file.readline().split(" ")]            
        self.robots = [[int(char) for char in file.readline().split(" ")] for i in range(int(file.readline()))]
        #invert y coordinate of robots for correct coordinate positioning
        for i in range(len(self.robots)):
            self.robots[i][1] = (self.dimensions[0] - 1) - self.robots[i][1]
        #create Nodes for robot paths
        self.robotNodes = []
        for robot in self.robots:
            self.robotNodes.append(Node(position=(robot[0],robot[1])))
        self.robots = self.robotNodes
        self.goal = [int(i) for i in file.readline().split(" ")]
        self.goal[1] = (self.dimensions[0] - 1) - self.goal[1]
        self.map = [[int(char) for char in line if char != '\n'] for line in file]
        self.offsetX = 0
        self.offsetY = 0
        self.visited = []
    
    def draw(self, surface, square):
        #draw black and white squares
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                color = WHITE
                if self.map[row][col] == 1:
                    color = BLACK
                the_square = ((col+self.offsetX)*square, (row+self.offsetY)*square, square, square)
                surface.fill(color, the_square)
                pygame.draw.rect(surface, BLACK, the_square, 1)       
        #draw goal square
        the_square = ((self.goal[0]+self.offsetX)*square, (self.goal[1]+self.offsetY)*square, square, square)
        surface.fill(GOLD, the_square)
        pygame.draw.rect(surface, BLACK, the_square, 1)
        #draw current robot paths
        for i in range(len(self.robots)):
            rect = pygame.Surface((square,square), pygame.SRCALPHA, 32)
            rect.fill(COLORS[i])
            currentNode = self.robots[i]
            while currentNode is not None:
                robot_pos = currentNode.position
                surface.blit(rect, ((robot_pos[0]+self.offsetX)*square, (robot_pos[1]+self.offsetY)*square))
                currentNode = currentNode.child
        #draw all visited points
        for point in self.visited:
            rect = pygame.Surface((square,square), pygame.SRCALPHA, 32)
            rect.fill(VISITED)
            robot_pos = point
            surface.blit(rect, ((robot_pos[0]+self.offsetX)*square, (robot_pos[1]+self.offsetY)*square))
    
    #prints details of map, used in debugging
    def printDetails(self):
        print()
        #print(self.dimensions)
        #print(self.robots)
        #print(self.goal)
        #for i in range(len(self.map)):
        #    for j in range(len(self.map[0])):
        #        print(self.map[i][j], end=", ")
        #    print()
            
