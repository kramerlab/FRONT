from FRONT.Forest.Trees.RSTree import RSTree
from FRONT.Forest.Trees.NTree import NTree
import numpy as np

# Node Object for an RS-Tree
#
class Forest(object):
    def __init__(self, bins,bounds,max_depth,trees,profileMode='classic',profileArgs="",subtree=False,tree=False):
        self.trees=[]
        self.bounds=bounds
        for i in range(0,trees):
            if tree == "RSTree":
                self.trees.append(RSTree(bins,self.bounds,max_depth,profileMode,profileArgs,subtree))
            elif tree == "NTree":
                self.trees.append(NTree(bins, self.bounds, max_depth, profileMode, profileArgs, subtree))
            else:
                raise ValueError("Unrecognized Tree Type")
        self.counter=0
        self.profileMode=profileMode
    def toString(self,index=0):
        return str(self.trees[index])


    def updateProfile(self,x):
        for i in self.trees:
            i.updateProfile(x)

    # Not used anymore, moved these to the Tree Level, less efficient but allows a Modular Construction of the Tree
    # def updateBatchVolume(self):
    #     volume = np.float64(1)
    #     for i in self.tempBounds:
    #         volume = volume * np.ptp(i)
    #     self.batchVolume=volume
    #
    # def updateBounds(self):
    #     data=np.array(self.buffer)
    #     bounds = []
    #     means = np.mean(data, axis=0)
    #     stds = np.std(data, axis=0)
    #     self.mins=means-4.645 * stds
    #     self.maxs=means + 4.645 * stds
    #     for i in range(0, data.shape[1]):
    #         bounds.append([self.mins[i],self.maxs[i]])
    #     self.tempBounds=bounds
    #     self.updateBatchVolume()

    def getTransform(self,x):
        if hasattr(self,"mins") and hasattr(self,"maxs"):
            return (x-self.mins/(self.maxs-self.mins))
        else:
            return np.zeros(len(x))


    def Score(self,x,nodeSizeLimit=0.1):
        #print "this shouldN#t come"
        out=np.float64(0)
        for i in self.trees:
            out+=i.Score(x,nodeSizeLimit)
        return out/len(self.trees)


    def feed(self,x,nodeSizeLimit=0.1):
        out=np.float64(0)
        for i in self.trees:
            out+=i.feed(x,nodeSizeLimit)
        return out/len(self.trees)
