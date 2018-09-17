from FRONT.Forest.Trees.Nodes.RSNode import *
class RSTree(object):
    def __init__(self, bins,bounds,max_depth,profileMode,profileArgs,subtree):
        self.bounds=bounds
        self.depth = max_depth
        self.root = Node(bins,self.bounds,0,max_depth,None,profileMode=profileMode,profileArgs=profileArgs)
        self.subtree=subtree
        self.subtreeVolume=self.root.v

    def __str__(self):
        return str(self.root)

    def Score(self, x, nodeSizeLimit):
        node = self.root.getLeaf(x, self.root.getNodeProfile()*nodeSizeLimit)
        if self.subtree:
            return node.getScore(self.root.getNodeProfile())*(self.root.v/self.subtreeVolume)
        else:
            out = node.getScore(self.root.getNodeProfile())
            return out

    def switchProfile(self):
        self.root.switchProfile()
        if self.subtree == True:
            self.subtreeVolume=self.root.findSplit().v

    def updateProfile(self, x):
        self.root.updateProfile(x)
        if self.root.profile.getUpdatePoint():
            self.switchProfile()

    def feed(self,x,nodeSizeLimit):
        out = self.Score(x, nodeSizeLimit)
        self.updateProfile(x)
        return out

