import pygame,sys
import numpy as np
from settings import *
from cell import cell,smartCell

def randPos(num,Type):
    l=[]
    for i in xrange(num):
        x=np.random.random()*width
        y=np.random.random()*height
        l.append(Type((x,y)))

    return l

class cellList:
    def __init__(self,num,numFood):
        self.cells=randPos(num,smartCell)
        self.generation=[]

        self.foodList=randPos(numFood,cell)

    def frames(self):
        for f in self.foodList:
            f.frame()
        
        dead=[]
        for i,c in enumerate(self.cells):
            ind=c.frame(self)
            
            if not ind==None:#some food was eaten,get rid of it
                del self.foodList[ind]

            if c.dead:
                dead.append(c)
                self.generation.append((c.fitness,c))

        nonDead=[x for x in self.cells if not x.dead]
        self.cells=nonDead
        for c in dead:
            c.erase()
        #do i need to return those things?
                
            
    def closestFood(self,x,y):
        cdist=10**10
        cell=None
        ind=None

        for i,c in enumerate(self.foodList):
            if not c.dead:
                dist=(c.x-x)**2+(c.y-y)**2
                if dist<cdist:
                    cdist=dist
                    cell=c
                    ind=i

        return [ind,cell]

    
    
    def runGen(self):
        #runs until all of the cells in this set are dead.
        #populates the cellList generation attribute with a list of cells and their fitness
        while len(self.cells)>0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.frames()
            pygame.display.flip()

    def breed(self):
        print 'nope'
        #breeds all of the cells in a cellList (that has been run thorugh a generation) selectivly based on fitness
        #returns new cellList of the offspring with some mutations
