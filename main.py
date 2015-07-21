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
width = 800
height = 600

#creating the pygame screen
screen = pygame.display.set_mode((width, height))
bgColor=(0,0,0)
screen.fill(bgColor)

class brain:
    #brains consist of layers of neurons (which are just vectors) connected by
    #synapses (wights) 
    def __init__(self,nInput,nOutput,nHiddenLayers,numPerHiddenLayer):
        self.syn=randomSyn(nInput,nOutput,nHiddenLayers,numPerHiddenLayer)

    def evaluate(self,In):
        curr=In
        for layer in self.syn:
            curr=np.dot(layer,curr)

        return curr

def randomSyn(nInput,nOutput,nHiddenLayers,numPerHiddenLayer):
    syn=[]
    for i in xrange(nHiddenLayers):
        syn.append(2*np.random.random((numPerHiddenLayer,nInput))-1)
    syn.append(2*np.random.random((nOutput,numPerHiddenLayer))-1)

    return syn

class cell:
    #basic unit of the game
    def __init__(self,(x,y),(v,angle),mass):
        self.x=x
        self.y=y
        self.v=v
        self.angle=angle
        self.color=(255,0,0)
        self.thickness=1
        self.mass=mass

        #dead attribute is used to mark cells so that they can be taken out
        #of the cells list once they have been eaten
        self.dead=False

    #determines radius based on mass
    def getRad(self):
        return self.mass/2
    
    #draws a circle representing the cell
    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x),int(self.y)), int(self.getRad()), self.thickness)

    #draws a circle in the same position as the cell but in the background color
    #hopefully this method is faster than drawing over the entire screen with
    #screen.fill(bgColor)
    def erase(self):
        pygame.draw.circle(screen, bgColor, (int(self.x),int(self.y)), int(self.getRad()), self.thickness)

    #uses the cells velocity to change the cells position
    #assumes constant velocity
    def move(self):
        self.x+=self.v * math.cos(self.angle)
        self.y-=self.v * math.sin(self.angle)

    #keeps cells within the bounding box
    def bounce(self):
        if self.x > width - self.getRad():
            self.x = 2*(width - self.getRad()) - self.x
            self.angle = math.pi - self.angle
        elif self.x < self.getRad():
            self.x = 2*self.getRad() - self.x
            self.angle = math.pi - self.angle
     
        if self.y > height - self.getRad():
            self.y = 2*(height - self.getRad()) - self.y
            self.angle = - self.angle
     
        elif self.y < self.getRad():
            self.y = 2*self.getRad() - self.y
            self.angle = - self.angle

    #larger cells absorb smaller cells
    def absorb(self,other):
        diff=2#difference required to be able to absorb the smaller cell
        
        small=None
        big=None
        if self.mass>other.mass+diff:
            small=other
            big=self
        elif other.mass>self.mass+diff:
            small=self
            big=other
        else:
            return False

        

        dist=(small.x-big.x)**2+(small.y-big.y)**2
        if dist<big.getRad()**2:
            #need to erase old cells
            small.erase()
            big.erase()

            #conservation of mass and momentum
            (angle,momentum)=addVectors((big.angle,big.v*big.mass),(small.angle,small.v*small.mass))
            big.mass=big.mass+small.mass
            big.angle=angle
            big.v=momentum/big.mass
            
            small.dead=True

            #draw new cell
            big.display()

            #cell was eaten return True
            return True
        return False
    
    def frame(self,cells):
        self.erase()
        self.move()
        self.bounce()
        self.display()


class food(cell):
    def __init__(self,(x,y)):
        self.x=x
        self.y=y
        self.color=(255,0,0)
        self.thickness=1
        self.mass=2

        #dead attribute is used to mark cells so that they can be taken out
        #of the cells list once they have been eaten
        self.dead=False

    def frame(self):
        self.erase()
        self.display()

class smartCell(cell):
    def __init__(self,(x,y)):
        self.brain=brain(4,4,1,5)
        self.health=100.0
        
        self.x=x
        self.y=y
        self.color=(255,0,0)
        self.thickness=1
        self.mass=20

        #dead attribute is used to mark cells so that they can be taken out
        #of the cells list once they have been eaten
        self.dead=False

    def move(self,In):
        #right,down,left,up
        out=self.brain.evaluate(In)
        m=np.argmax(out)
        if m==0:
            self.x+=1
        elif m==1:
            self.y+=1
        elif m==2:
            self.x-=1
        elif m==3:
            self.y-=1

    def bounce(self):
        if self.x > width - self.getRad():
            self.x = 2*(width - self.getRad()) - self.x
        elif self.x < self.getRad():
            self.x = 2*self.getRad() - self.x
     
        if self.y > height - self.getRad():
            self.y = 2*(height - self.getRad()) - self.y
     
        elif self.y < self.getRad():
            self.y = 2*self.getRad() - self.y

    def absorb(self,f):
        
        dist=(self.x-f.x)**2+(self.y-f.y)**2
        if dist<self.getRad()**2:
            print 'eat stuff'
            #need to erase old food
            f.erase()
            
            f.dead=True

            #draw new cell
            self.display()

            #cell was eaten return True
            return True
        return False

    def frame(self,foodList):
        self.erase()

        cfood=findClosest(foodList,self.x,self.y)
        In=[cfood.x,cfood.y,self.x,self.y]
        self.move(In)


        self.bounce()
        self.display()

def findClosest(cellList,x,y):
    cdist=10**10
    cell=None

    for c in cellList:
        dist=(c.x-x)**2+(c.y-y)**2
        if dist<cdist:
            cdist=dist
            cell=c

    return cell

    
def addVectors((a1,l1),(a2,l2)):
    x  = math.sin(a1) * l1 + math.sin(a2) * l2
    y  = math.cos(a1) * l1 + math.cos(a2) * l2

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

def randCellList(num):
    cells=[]
    for i in xrange(num):
        v=random()
        a=uniform(0,math.pi*2)
        x=random()*width
        y=random()*height
        m=random()*10+5
        cells.append(cell((x,y),(v,a),m))

    return cells

def randFood(num):
    f=[]
    for i in xrange(num):
        x=random()*width
        y=random()*height
        f.append(food((x,y)))

    return f

def randPos(num,Type):
    l=[]
    for i in xrange(num):
        x=random()*width
        y=random()*height
        l.append(Type((x,y)))

    return l
                 


#cells=randCellList(20)
"""
testa=7*math.pi/6
rad=150
x=width/2
y=height/2
cells=[cell((x-rad*math.cos(testa),y+rad*math.sin(testa)),(.2,testa),10), cell((x+rad*math.cos(testa),y-rad*math.sin(testa)),(.6,math.pi+testa),5)]
"""
cells=randPos(20,smartCell)
foodList=randPos(100,food)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    deadCells=[]
    for i,c in enumerate(cells):
        if not c.dead:
            c.frame(foodList)
            cfood=findClosest(foodList,c.x,c.y)
            if not cfood.dead:
                c.absorb(cfood)
            
            
        if c.dead:
            deadCells.append(i)

    for i in deadCells:
        del cells[i]


    deadFood=[]
    for i,f in enumerate(foodList):
        if not f.dead:
            f.frame()

        if f.dead:
            deadFood.append(i)

    for i in deadFood:
        del foodList[i]

    pygame.display.flip()
