width = 800
height = 600
bgColor=(0,0,0)
displayStuff=True

minx=0
miny=0
maxx=800
maxy=600


numCells=20
numFood=20
numGenerations=30000

#cell
velocity=4
framesWithoutFood=400
maxHealth=100.0
healthSub=maxHealth/framesWithoutFood
#healthSub=0
maxTime=20

#brain
#inputs are x,y,deathState of food and its own xy coordinates
numInputs=8
numOutputs=2
numHiddenLayers=1
numPerHidden=6
if numHiddenLayers==0:
    numPerHidden=numInputs
totSyn=numInputs*numPerHidden+(numHiddenLayers-1)*numPerHidden**2+numPerHidden*numOutputs


#breeding
mutationRate=.25
