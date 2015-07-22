import numpy as np
from settings import *

def randomSyn(nInput,nOutput,nHiddenLayers,numPerHiddenLayer):
    syn=[]
    for i in xrange(nHiddenLayers):
        syn.append(2*np.random.random((numPerHiddenLayer,nInput))-1)
    syn.append(2*np.random.random((nOutput,numPerHiddenLayer))-1)

    return syn

"""
def mutate(syn):
    numMutate=int(totSyn*mutationRate)

    numLayers=len(syn)
    for i in xrange(numMutate):
        #choose a layer
        n=np.random.randint(0,numLayers)
        #choose a row
        r=np.random.randint(0,len(syn[n]))
        #choose a collumn
        c=np.random.randint(0,len(syn[n][r]))

        syn[n][r][c]=2*np.random.random()-1

    return syn
"""
def mutate(num):
    if np.random.random()<mutationRate:
        return num+(2*np.random.random()-1)
    return num


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

    def breed(self,other):
        #one position crossover//changed to random at every position
        #pick random position to switch from first brain to second
        #all breeding brains must be the same size
        numLayers=len(self.syn)

        #choose a layer
        #n=np.random.randint(0,numLayers)
        #choose a row
        #r=np.random.randint(0,len(self.syn[n]))
        #choose a collumn
        #c=np.random.randint(0,len(self.syn[n][r]))

        newSyn=[]
        for i in xrange(numLayers):
            """
            if i<n:
                newSyn.append(self.syn[i])
            elif i>n:
                newSyn.append(other.syn[i])
            else:
            """
            newlayer=[]
            for j in xrange(len(self.syn[i])):
                """
                if j<r:
                    newlayer.append(self.syn[i][j])
                elif j>r:
                    newlayer.append(other.syn[i][j])
                else:
                """
                newrow=[]
                for k in xrange(len(self.syn[i][j])):
                    if np.random.random()<=.5:
                        newrow.append(mutate(self.syn[i][j][k]))
                    else:
                        newrow.append(mutate(other.syn[i][j][k]))
                newlayer.append(newrow)

            newSyn.append(np.array(newlayer))
        
        #mutation
        #newSyn=mutate(newSyn)
        
        newbrain=brain(4,4,1,5)
        newbrain.syn=newSyn

        return newbrain

    def makeSuperSmart(self):
        s=np.zeros([numOutputs,numInputs])
        """
        #Four outputs
        s[0,0]=-1
        s[0,2]=1
        s[1,1]=-1
        s[1,3]=1
        s[2,0]=1
        s[2,2]=-1
        s[3,1]=1
        s[3,3]=-1
        """
        #two outputs
        s[0,0]=-1
        s[0,2]=1
        s[1,1]=-1
        s[1,3]=1

        self.syn=[s]
