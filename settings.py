width = 800
height = 600
bgColor=(0,0,0)


numCells=50
numFood=20
numGenerations=3000

#cell
velocity=10
framesWithoutFood=100
maxHealth=100.0
healthSub=maxHealth/framesWithoutFood

#brain
#inputs are x,y,deathState of food and its own xy coordinates
numInputs=numFood*2+2#4
numOutputs=4
numHiddenLayers=1
numPerHidden=5
totSyn=numInputs*numPerHidden+(numHiddenLayers-1)*numPerHidden**2+numPerHidden*numOutputs


#breeding
mutationRate=.05
