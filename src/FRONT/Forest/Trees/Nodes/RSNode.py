from Profiles.RSProfile import RSProfile
from FRONT.utils.utils import getNodeVolume
from FRONT.utils.utils import splitBounds
import numpy as np

class Node(object):
    #IN:
    # bounds= List of with number of dimensions numpy arrays each containing two values 1 for Lower BOund, 1 for upper bound
    # depth= Int current depth of the node
    # max depth= max depth of the tree
    # parent = parentNode
    def __init__(self, bins,bounds,depth, max_depth, parent,profileMode,profileArgs):
        self.parent=parent
        self.v=getNodeVolume(bounds)
        self.depth=depth
        if profileMode == "classic":
            self.profile=RSProfile(profileArgs)
        elif profileMode =="global":
            self.profile=GlobalProfile(profileArgs)
        if depth < max_depth:
            bounds_left,bounds_right,self.splitAtt,self.cutPoint=splitBounds(bounds)
            if bounds_left == None:
                self.splitAtt = None
                self.left = None
                self.right = None
                self.cutPoint = None
            else:
                self.left=Node(bins,bounds_left,depth+1,max_depth,self,profileMode,profileArgs)
                self.right=Node(bins,bounds_right,depth+1,max_depth,self,profileMode,profileArgs)
        else:
            self.splitAtt=None
            self.left=None
            self.right=None
            self.cutPoint=None





    # Ignore, just for Bugfixing

    def __str__(self, level=0, appendix=""):
        ret = "\t" * level + appendix + ' profile: ' + str(self.profile.getBins())+"|"+str(self.profile.bins) + ' v; ' + repr(self.v) + ' Atr: ' + repr(self.splitAtt) + ' cut: ' + repr(self.cutPoint) + "\n"
        if self.left is not None:
            ret += self.left.__str__(level=level + 1, appendix="left ")
        if self.right is not None:
            ret += self.right.__str__(level=level + 1, appendix="right ")
        return ret

    def __repr__(self):
        return '<tree node representation>'

    # Returns the root node of the smallest Subtree containing all the data points
    def findSplit(self):
        #print "finding Split:"
        if self.isLeaf():
           #print "reached Leaf:"
            return self
        else:
            if self.getNodeProfile() == self.left.getNodeProfile():
                return self.left.findSplit()
            elif self.getNodeProfile() == self.right.getNodeProfile():
                return self.right.findSplit()
            else:
                return self


    # if ml is true ml is updated, else mr is updated
    def updateProfile(self, x):
        self.profile.increment()
        if not self.isLeaf():
            self.getChild(x).updateProfile(x)

    def getChild(self, x):
            if (x[self.splitAtt] <= self.cutPoint):
                return self.left
            else:
                return self.right

    def isLeaf(self):
        if self.splitAtt is None:
            return True
        else:
            return False

    def getNodeProfile(self):
        return self.profile.getBins()

    def getLeaf(self, x, nodeSizeLimit):
        profile=self.getNodeProfile()
        if profile  == 0:
            if self.parent != None:
                return self.parent
            else:
                return self
        elif np.all(profile<=nodeSizeLimit):
            return self
        else:
            if self.isLeaf() is True:
                return self
            else:
                return self.getChild(x).getLeaf(x,nodeSizeLimit)


    def getLeafAndIncrement(self, x, nodeSizeLimit, ml):
        profile = self.getNodeProfile(ml)
        self.increment(ml)
        if np.all(profile<nodeSizeLimit):
            return self
        else:
            if self.isLeaf() is True:
                return self
            else:
                return self.getChild(x).getLeafAndIncrement(x,nodeSizeLimit,ml)

    def getScore(self,n):
        profile=self.getNodeProfile()
        return profile/(self.v*n)

    def switchProfile(self):
        self.profile.switchProfile()
        if not self.isLeaf():
            if not self.left.profile.isEmpty():
                 self.left.switchProfile()
            if not self.right.profile.isEmpty():
                 self.right.switchProfile()


if __name__ == "__main__":
    #For Testing purposes
    print ""