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
    
    next = np.ndarray(shape = (size))
    for x in range(rows):
        for y in range(columns):
        
            state = gridArray[x][y]
            neighbors = getNeighbors(x,y)
            if state == 1 and (neighbors <2 or neighbors >3):
                next[x][y] = 0
        #Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            elif state == 0 and neighbors == 3:
                next[x][y] =1
        #any live cell with fewer than two live neighbours dies as if by underpopulation
        # Any live cell with more than three live neighbours dies, as if by overpopulation.
            #Any live cell with two or three live neighbours lives on to the next generation.
            else:
                next[x][y] = state
    gridArray = next