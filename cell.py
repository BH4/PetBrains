from settings import *
from brain import brain
import numpy as np

class cell:
    screen=None
    
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
        pygame.draw.circle(cell.screen, self.color, (int(self.x),int(self.y)), int(self.getRad()), self.thickness)

    #draws a circle in the same position as the cell but in the background color
    #hopefully this method is faster than drawing over the entire screen with
    #screen.fill(bgColor)
    def erase(self):
        pygame.draw.circle(cell.screen, bgColor, (int(self.x),int(self.y)), int(self.getRad()), self.thickness)
    
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
            #need to erase old food
            f.erase()
            
            f.dead=True

            #draw new cell
            self.display()
            self.health=100.0

            #cell was eaten return True
            return True
        return False

    def frame(self,foodList):
        self.health-=.1
        if self.health<=0:
            self.dead=True
        
        self.erase()

        [ind,cfood]=foodList.closest(self.x,self.y)
        In=[cfood.x,cfood.y,self.x,self.y]
        self.move(In)

        #test if i am close enough to eat that close food
        eaten=self.absorb(cfood)

        self.bounce()
        self.display()

        if eaten:
            return ind
        return None