import numpy as np
import shlex
#Profile Used for Batch data
class GlobalProfile:
    def __init__(self,profileArgs):
        self.bins = np.zeros(1)

    def increment(self):
        self.bins +=1


    def switchProfile(self):
        pass

    def getBins(self):
        return self.bins

    def getUpdatePoint(self):
        return False

    def isEmpty(self):
        return np.all(self.bins == 0)

    def __str__(self):
        return str(self.bins)


if __name__ == "__main__":
    #For Test Purposes only
    s="size=512"
    args = dict(token.split('=') for token in shlex.split(s))
    print args



    
