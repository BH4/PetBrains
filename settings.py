width = 800
height = 600
bgColor=(0,0,0)


numCells=10
numFood=20
numGenerations=3000

#cell
velocity=1
framesWithoutFood=500
maxHealth=100.0
#healthSub=maxHealth/framesWithoutFood
healthSub=0

#brain
#inputs are x,y,deathState of food and its own xy coordinates
numInputs=4
numOutputs=4
numHiddenLayers=0
numPerHidden=5
if numHiddenLayers==0:
    numPerHidden=numInputs
totSyn=numInputs*numPerHidden+(numHiddenLayers-1)*numPerHidden**2+numPerHidden*numOutputs


#breeding
mutationRate=.05
