from FRONT.Forest.Trees.RSTree import *
class NTree(RSTree):
    def __init__(self, bins,bounds,max_depth,profileMode,profileArgs,subtree):
        self.bounds = [np.array([0, 1], dtype=np.float64) for i in range(0, len(bounds))]
        self.depth = max_depth
        self.root = Node(bins,self.bounds,0,max_depth,None,profileMode=profileMode,profileArgs=profileArgs)
        self.subtree=subtree
        self.subtreeVolume=self.root.v
        self.buffer = []
        self.batchVolume=1
        self.updateBatchVolume()

    def updateBatchVolume(self):
        volume = np.float64(1)
        for i in self.bounds:
            volume = volume * np.ptp(i)
        self.batchVolume=volume

    def updateBounds(self):
        data=np.array(self.buffer)
        bounds = []
        means = np.mean(data, axis=0)
        stds = np.std(data, axis=0)
        self.mins=means-4.645 * stds
        self.maxs=means + 4.645 * stds
        for i in range(0, data.shape[1]):
            bounds.append([self.mins[i],self.maxs[i]])
        self.bounds=bounds
        self.updateBatchVolume()

    def getTransform(self,x):
        if hasattr(self,"mins") and hasattr(self,"maxs"):
            return (x-self.mins)/(self.maxs-self.mins)
        else:
            return np.zeros(len(x))

    def updateProfile(self, x):
        self.buffer.append(x)
        if self.root.profile.updatePoint == len(self.buffer):
            self.updateBounds()
            for i in self.buffer:
                self.root.updateProfile(self.getTransform(i))
            self.switchProfile()
            self.buffer=[]

    def feed(self,x,nodeSizeLimit):
        out = self.Score(x, nodeSizeLimit)
        self.updateProfile(x)
        return out

    def Score(self, x, nodeSizeLimit):
        node = self.root.getLeaf(self.getTransform(x), self.root.getNodeProfile()*nodeSizeLimit)
        if self.subtree:
            out = node.getScore(self.root.getNodeProfile())*(self.root.v/self.subtreeVolume)
        else:
            out = node.getScore(self.root.getNodeProfile())
        if self.batchVolume == 0:
            return 1
        else:
            return out/self.batchVolume

