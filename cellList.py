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

def findInWheel(a,lis):
    #need to find the index of the first element of the roulette wheel which is greater than a
    #once we find this then we return this index -1 so that the number coresponds to
    #the index of the correct cell in the generation list
    lam=lambda x:a<x
    ind=(i for i,v in enumerate(lis) if lam(v)).next()
    return ind-1

class cellList:
    def __init__(self,num,numFood):
        self.cells=randPos(num,smartCell)
        self.generation=[]

        self.foodList=randPos(numFood,cell)

    def frames(self):
        for f in self.foodList:
            if not f.dead:
                f.frame()
        
        dead=[]
        for i,c in enumerate(self.cells):
            ind=c.frame(self)

            if not ind==None:#some food was eaten,get rid of it
                self.foodList[ind].reset()

            if c.dead:
                dead.append(c)
                self.generation.append((c.fitness,c))

        nonDead=[x for x in self.cells if not x.dead]
        self.cells=nonDead
        for c in dead:
            c.erase()

                
            
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

        s=sorted(self.generation)[-1]
        return s

    def breed(self):
        #breeds all of the cells in a cellList (that has been run thorugh a generation) selectivly based on fitness
        #returns new cellList of the offspring with some mutations
        newCells=[]

        
        #select only top 10 for some reason
        n=[]
        self.generation.sort(reverse=True)
        for i in xrange(10):
            n.append(self.generation[i])
        self.generation=n

        g=lambda x:x[0]
        totFit=sum(map(g,self.generation))

        rouletteWheel=[0.0]
        for i,c in enumerate(self.generation):
            rouletteWheel.append(rouletteWheel[i]+c[0]/totFit)

        
        #print rouletteWheel
        for i in xrange(numCells):
            a=np.random.random()
            b=np.random.random()
            indA=findInWheel(a,rouletteWheel)
            indB=findInWheel(b,rouletteWheel)
            
            #print a
            #print indA
            
            x=np.random.random()*width
            y=np.random.random()*height
            newCells.append(self.generation[indA][1].breed(self.generation[indB][1],(x,y)))

        #reset this cellList
        self.cells=newCells
        self.generation=[]
        self.foodList=randPos(numFood,cell)







        
