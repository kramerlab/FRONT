import numpy as np
from FRONT.Forest.Trees.RSTree import *
from FRONT.Forest.RSForest import *


# Node Object for an RS-Tree
#
class NBForest(Forest):
    def __init__(self, bins,bounds,max_depth,trees,profileMode='classic',profileArgs="",subtree=False,tree=False):
        dims=len(bounds)
        self.treeList = self.getTreeDistribution(trees,dims)
        self.trees=[None for i in range(0,trees)]
        for i in range(0,len(self.treeList)):
            for j in self.treeList[i]:
                self.trees[j]="blubb" #Need to initiliaze something
                if tree == "RSTree":
                    self.trees[j]=RSTree(bins,[bounds[i]],max_depth,profileMode,profileArgs,subtree)
                elif tree == "NTree":
                    self.trees[j] = NTree(bins, [bounds[i]], max_depth, profileMode, profileArgs, subtree)
                else:
                    raise ValueError("Unrecognized Tree Type")
        self.bounds=bounds
        self.counter=0
        self.profileMode=profileMode

    def updateProfile(self,x):
        for i in range(0,len(self.treeList)):
            for j in self.treeList[i]:
                self.trees[j].updateProfile([x[i]])

    # Used in Init and divides the available number of Trees  M across dimensions d, case d>M not yet implemented
    def getTreeDistribution(self,trees,dims):
        treeList=np.zeros(dims,dtype=int)
        idx=0
        while trees >0:
            treeList[idx % dims]+=1
            trees -=1
            idx +=1
        out=[]
        temp=0
        for i in treeList:
            out.append(range(temp,temp+i))
            temp=temp+i
        print "TreeList: ",treeList
        print "Out: ",out
        return out


    def Score(self,x,nodeSizeLimit=0.1):
        out=np.float64(1)
        for i in range(0,len(self.treeList)):
            tmp=np.float64(0)
            for j in self.treeList[i]:
                tmp+=self.trees[j].Score([x[i]],nodeSizeLimit)
            out*=tmp/len(self.treeList[i])
        return out

    def feed(self,x,nodeSizeLimit=0.1):
        out=np.float64(1)
        for i in range(0,len(self.treeList)):
            tmp=np.float64(0)
            for j in self.treeList[i]:
                tmp+=self.trees[j].feed([x[i]],nodeSizeLimit)
            out*=tmp/len(self.treeList[i])
        return out
