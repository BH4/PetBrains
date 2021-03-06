#next steps
#increase the size of the space cells can move in
#make it so the field of view can change by using the mouse
#change settings so that it ends up being less dense with cells

from time import time
import pygame,sys
import numpy as np
from random import random, uniform
import math
from brain import brain
from cellList import cellList
from cell import cell,smartCell

from settings import *

screen = pygame.display.set_mode((width, height))
if displayStuff:
    
    screen.fill(bgColor)
    screenPos=[0,0]

    #we need to pass the screen to the cell class so that it can use it.
    cell.screen=screen
    cell.screenPos=screenPos

pets=cellList(numCells,numFood)

maxFitList=[]
t=time()
stats=pets.runGen()
for i in xrange(numGenerations-1):
    if displayStuff:
        screen.fill(bgColor)

    maxFitList.append(stats)
    nt=time()
    string="Generation " + str(i) + ": Max Fitness="+str(stats[0])+": Time to Run="+str(int(nt-t))
    t=nt
    print string
    pets.breed()
    stats=pets.runGen()

maxFitList.append(stats)
string="Generation " + str(i) + ": Max Fitness="+str(stats[0])
print string

    
pygame.quit()
sys.exit()
