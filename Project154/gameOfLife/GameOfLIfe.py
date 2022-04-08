import pygame
import time
import random
import numpy as np
import os

class Grid:
    def __init__(self, width, height, scale, offset):
        self.scale = scale

        self.columns = int(height/scale)
        self.rows = int(width/scale)

        self.size = (self.rows, self.columns)
        self.matrix = np.ndarray(self.size)
        self.offset = offset

    def gridInit(self):
        '''
        we need to setup and intialize a matrix for dynamic lookups. 
        '''
        for x in range(self.rows):
            for y in range(self.columns):
                self.matrix[x][y] = random.randint(0,1)


    def rules(self, off, on, surface, pause):
        diff = self.scale-self.offset

        for x in range(self.rows):
            for y in range(self.columns):
                #scale is the length of one box in pygame. This helps establishes the x and y for the board. 
                yPos = y * self.scale
                xPos = x * self.scale
                #What this does is it draws on the board when a box is selected(on) or when it is not selected(off)
                if self.matrix[x][y] == 1: 
                    pygame.draw.rect(surface, on, [xPos, yPos, diff, diff])
                else:
                    pygame.draw.rect(surface, off, [xPos, yPos, diff, diff])
        #temp matrix to look at the next state
        temp = np.ndarray(self.size)

        if pause == False:
            for x in range(self.rows):
                for y in range(self.columns):
                    state = self.matrix[x][y] #current state
                    neigh = self.getNeigh( x, y) #neighboring states

                    #Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                    if state == 1 and neigh < 2:
                        temp[x][y] = 0
                    #Any live cell with more than three live neighbours dies, as if by overpopulation.
                    elif state == 1 and neigh > 3:
                        temp[x][y] = 0
                    #Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                    elif state == 0 and neigh == 3:
                        temp[x][y] = 1
                    #Any live cell with two or three live neighbours lives on to the next generation.
                    else:
                        temp[x][y] = state
            self.matrix = temp #change the matrix based on the rules
        

    def getNeigh(self, x, y):
        total = 0
        for n in range(-1, 2):
            for m in range(-1, 2):
                xEdge = (x+n+self.rows) % self.rows #x is location of you + an increment surround the area + the rows for the modular to keep it in the boundaries
                yEdge = (y+m+self.columns) % self.columns
                total += self.matrix[xEdge][yEdge] #find total to pass thru the rules. Counts the number of neighbors
            

        total -= self.matrix[x][y] #iterate thru each and decrement 
        return total


os.environ["SDL_VIDEO_CENTERED"]='1'

#resolution
width, height = 1920,1080
size = (width, height)

pygame.init()
pygame.display.set_caption("Conway's Game OF Life")
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 30

black = (0, 0, 0)
white = (255, 255, 255)

scaler = 15
offset = 1

Grid = Grid(width,height, scaler, offset)
Grid.gridInit()

pause = False
run = True
while run:
    clock.tick(fps)
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                pause = not pause
    
    Grid.rules(white, black, screen, pause)


    pygame.display.update()

pygame.quit()