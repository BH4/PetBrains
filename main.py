#next steps
#create a cell that i can control
#center screen on my cell and allow cells to move outside of screen (difficult)
#give cells ai so they try to eat the closest smaller cell
#give cells a max speed based on their mass
#make dumb cells that are smaller than initial smart cells. dumb cells dont move


import pygame,sys
import numpy as np
from random import random, uniform
import math
from brain import brain
from cellList import cellList
from cell import cell,smartCell

from settings import *
screen = pygame.display.set_mode((width, height))
screen.fill(bgColor)

#we need to pass the screen to the cell class so that it can use it.
cell.screen=screen


pets=cellList(20,smartCell)
foods=cellList(100,cell)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    pets.frames(foods)
    pygame.display.flip()

    
