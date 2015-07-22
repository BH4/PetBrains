width = 800
height = 600
bgColor=(0,0,0)


numCells=20
numFood=100
numGenerations=1000

#cell
velocity=3
framesWithoutFood=50
maxHealth=100.0
healthSub=maxHealth/framesWithoutFood

#brain
numInputs=4
numOutputs=4
numHiddenLayers=1
numPerHidden=5
totSyn=numInputs*numPerHidden+(numHiddenLayers-1)*numPerHidden**2+numPerHidden*numOutputs


#breeding
mutationRate=.05
