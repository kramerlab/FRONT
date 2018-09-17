import numpy as np
import shlex
class RSProfile:
    def __init__(self,profileArgs):
        args=dict(token.split('=') for token in shlex.split(profileArgs))
        self.updatePoint=int(args['size'])
        self.bins = np.zeros(2, dtype=np.uint32)
        self.profile=0

    def increment(self):
        self.bins[self.profile] +=1


    def switchProfile(self):
        self.bins[(self.profile + 1) % 2] = 0
        self.profile = (self.profile + 1) % 2

    def getBins(self):
        return np.array(self.bins[(self.profile +1)%2])

    def getUpdatePoint(self):
        return self.bins[self.profile] % self.updatePoint == 0

    def isEmpty(self):
        return np.all(self.bins == 0)

    def __str__(self):
        return str(self.bins)


if __name__ == "__main__":
    #For test Purpose Only
    s="size=512"
    args = dict(token.split('=') for token in shlex.split(s))
    print args



    
