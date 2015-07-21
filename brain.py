import numpy as np

def randomSyn(nInput,nOutput,nHiddenLayers,numPerHiddenLayer):
    syn=[]
    for i in xrange(nHiddenLayers):
        syn.append(2*np.random.random((numPerHiddenLayer,nInput))-1)
    syn.append(2*np.random.random((nOutput,numPerHiddenLayer))-1)

    return syn

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

