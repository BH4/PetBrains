import numpy as np
from settings import *

def randPos(num,Type):
    l=[]
    for i in xrange(num):
        x=np.random.random()*width
        y=np.random.random()*height
        l.append(Type((x,y)))

    return l

class cellList:
    def __init__(self,num,Type):
        self.cells=randPos(num,Type)

    def frames(self,foodList):
        for f in foodList.cells:
            f.frame()
        
        dead=[]
        for i,c in enumerate(self.cells):
            ind=c.frame(foodList)
            
            if not ind==None:#some food was eaten,get rid of it
                del foodList.cells[ind]

            if c.dead:
                dead.append(c)

        nonDead=[x for x in self.cells if not x.dead]
        self.cells=nonDead
        for c in dead:
            c.erase()
        #do i need to return those things?
                
            
    def closest(self,x,y):
        cdist=10**10
        cell=None
        ind=None

        for i,c in enumerate(self.cells):
            if not c.dead:
                dist=(c.x-x)**2+(c.y-y)**2
                if dist<cdist:
                    cdist=dist
                    cell=c
                    ind=i

        return [ind,cell]

