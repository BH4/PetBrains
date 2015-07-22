width = 800
height = 600
bgColor=(0,0,0)


numCells=50
numFood=5
numGenerations=3000

#cell
velocity=1
framesWithoutFood=800
maxHealth=100.0
healthSub=maxHealth/framesWithoutFood
#healthSub=0
maxTime=20

#brain
#inputs are x,y,deathState of food and its own xy coordinates
numInputs=4
numOutputs=2
numHiddenLayers=0
numPerHidden=5
if numHiddenLayers==0:
    numPerHidden=numInputs
totSyn=numInputs*numPerHidden+(numHiddenLayers-1)*numPerHidden**2+numPerHidden*numOutputs


#breeding
mutationRate=.05
