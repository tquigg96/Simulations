import pygame
import time
import random
import numpy as np
import os
import grid

width, height, scale, offset= 1920, 1080, 40, 1
columns = int(height/2)
rows = int(width/2)


class

def randomArray():
    #randomly assigns on and off to automatically simulate game of life mechanics
    gridArray = np.ndarray((rows,columns))
    for x in range(rows):
        for y in range(columns):
            gridArray[x][y] = random.randint(0,1)
    return gridArray

def rules(gridArray, off, on, surface):
    for i in range(0,rows):
        for j in range(0,columns):
            x,y = i * scale, j*scale
            #sets up display for when square is filled
            if(gridArray[i][j] == 1):
                diff = scale - offset #Oh weird
                pygame.draw.rect(surface, on, [x,y, scale - offset, scale - offset])
            else:
                pygame.draw.rect(surface, off, [x,y, scale-offset, scale-offset])
    
    next = np.ndarray(shape = (rows,columns))
    for x in range(rows):
        for y in range(columns):
        
            state = gridArray[x][y]
            neighbors = getNeighbors(x,y)
            if state == 0 and neighbours == 3:
                next[x][y] = 1
        #Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
           elif state == 1 and (neighbours < 2 or neighbours > 3):
                next[x][y] = 0
        #any live cell with fewer than two live neighbours dies as if by underpopulation
        # Any live cell with more than three live neighbours dies, as if by overpopulation.
            #Any live cell with two or three live neighbours lives on to the next generation.
            else:
                next[x][y] = state
    gridArray = next

def getNeighbors( x, y):
    total = 0
    for n in range(-1, 2):
        for m in range(-1, 2):
            xEdge = (x+n+rows) % rows
            yEdge = (y+m+columns) % columns
            total += gridArray[xEdge][yEdge]
    total -= gridArray[x][y]
    return total

os.environ["SDL_VIDEO_CENTERED"] = '1'

width, height, scaler = 1920, 1080, 40
size = (width, height)

pygame.init()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
fps = 60

black = (0,0,0)
blue = (0,14,71)
white = (255,255,255)

gridArray = randomArray()
run = True
while run:
    clock.tick(fps)
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    rules(gridArray, white, blue, screen)

    if pygame.mouse.get_pressed()[0]:
        mX, mY = pygame.mouse.get_pos()
        _x, _y = mX//scale, mY//scale

        if gridArray[_x][_y] != None:
            gridArray[_x][_y] = 1
    pygame.display.update()
pygame.quit()