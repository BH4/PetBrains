from settings import *
from brain import brain
import numpy as np
import pygame

def colorSelector(c1,c2):
    if c1[2]==255 or c2[2]==255:
        return (0,0,255)
    return (255,0,0)


class cell:
    screen=None
    #top left corner of the screen
    screenPos=None
    
    #basic unit of the game
    def __init__(self,(x,y)):
        self.x=x
        self.y=y
        self.color=(255,0,0)
        self.thickness=1
        self.mass=2


        #dead attribute is used to mark cells so that they can be taken out
        #of the cells list once they have been eaten
        self.dead=False

    #determines radius based on mass
    def getRad(self):
        return self.mass/2
    
    #draws a circle representing the cell
    def display(self):
        if displayStuff:
            pygame.draw.circle(cell.screen, self.color, (int(self.x-cell.screenPos[0]),int(self.y-cell.screenPos[1])), int(self.getRad()), self.thickness)

    #draws a circle in the same position as the cell but in the background color
    #hopefully this method is faster than drawing over the entire screen with
    #screen.fill(bgColor)
    def erase(self):
        if displayStuff:
            pygame.draw.circle(cell.screen, bgColor, (int(self.x-cell.screenPos[0]),int(self.y-cell.screenPos[1])), int(self.getRad()), self.thickness)
    
    def frame(self):
        self.erase()
        self.display()

    def reset(self):
        self.x=np.random.random()*(maxx-minx)+minx
        self.y=np.random.random()*(maxy-miny)+miny
        self.dead=False


class smartCell(cell):
    def __init__(self,(x,y)):
        self.brain=brain(numInputs,numOutputs,numHiddenLayers,numPerHidden)
        self.health=maxHealth
        
        self.x=x
        self.y=y
        self.color=(255,0,0)
        self.thickness=1
        self.mass=20

        self.fitness=0.0

        #dead attribute is used to mark cells so that they can be taken out
        #of the cells list once they have been eaten
        self.dead=False

    def move(self,In):
        #right,down,left,up
        out=self.brain.evaluate(In)

        #normalize vector to correct length
        mag=np.sqrt(out[0]**2+out[1]**2)
        const=velocity/mag
        out[0]*=const
        out[1]*=const

        self.x+=out[0]
        self.y+=out[1]
        """
        m=np.argmax(out)
        if m==0:
            self.x+=velocity
        elif m==1:
            self.y+=velocity
        elif m==2:
            self.x-=velocity
        elif m==3:
            self.y-=velocity
        """

    def bounce(self):
        """
        if self.x > width:
            self.erase()
            self.x = self.x-width
            self.display()
        elif self.x < 0:
            self.erase()
            self.x = width+self.x
            self.display()
     
        if self.y > height:
            self.erase()
            self.y = self.y-height
            self.display()
     
        elif self.y < 0:
            self.erase()
            self.y = height+self.y
            self.display()
        """
        if self.x > maxx - self.getRad():
            self.x = 2*(maxx - self.getRad()) - self.x
        elif self.x < minx + self.getRad():
            self.x = 2*(minx + self.getRad()) - self.x
     
        if self.y > maxy - self.getRad():
            self.y = 2*(maxy - self.getRad()) - self.y
        elif self.y < miny + self.getRad():
            self.y = 2*(miny + self.getRad()) - self.y
        

    def absorb(self,f):
        
        dist=(self.x-f.x)**2+(self.y-f.y)**2
        if dist<self.getRad()**2:
            #need to erase old food
            f.erase()
            
            f.dead=True

            #draw new cell
            self.display()
            self.health=100.0
            self.fitness+=1

            #cell was eaten return True
            return True
        return False

    def frame(self,cells):
        self.health-=healthSub
        if self.health<=0:
            self.dead=True
        
        self.erase()

        [ind,cfood]=cells.closestFood(self.x,self.y)
        foodList=cells.foodList
        In=[self.x,self.y,cfood.x,cfood.y,minx,miny,maxx,maxy]
        """
        for f in foodList:
            In.append(f.x)
            In.append(f.y)
        """

        self.move(In)

        #test if i am close enough to eat that close food
        eaten=self.absorb(cfood)

        self.bounce()
        self.display()

        if eaten:
            return ind
        return None


    def breed(self,other,pos):
        newCell=smartCell(pos)
        newBrain=self.brain.breed(other.brain)
        newCell.brain=newBrain

        newCell.color=colorSelector(self.color,other.color)

        return newCell

    def makeSuperSmart(self):
        self.brain.makeSuperSmart()
        self.color=(0,0,255)



        
