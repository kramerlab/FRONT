import numpy as np
import random
import copy

def splitBounds(bounds):
    dims=getSplitableDims(bounds)
    if len(dims) > 0:
        splitAtt = dims[random.randint(0, len(dims) - 1)]
        out_left=copy.deepcopy(bounds)
        out_right=copy.deepcopy(bounds)
        limits=np.copy(bounds[splitAtt])
        type=limits.dtype
        if np.issubdtype(type,np.int):
            p=np.random.randint(limits[0],limits[1],dtype=np.int)
            out_left[splitAtt][1]=p
            out_right[splitAtt][0]=p+1
        elif np.issubdtype(type,np.float):
            p=np.random.uniform(limits[0],limits[1])
            out_left[splitAtt][1]=p
            out_right[splitAtt][0]=p
        else:
            print "error:"
            print splitAtt, type

        return out_left,out_right,splitAtt,p
    return None, None, None, None

def getSplitableDims(bounds):
    out=[]
    for i in range(0,len(bounds)):
        if bounds[i].dtype==np.float:
            out.append(i)
        else:
            if bounds[i][0] < bounds[i][1]:
                out.append(i)
    return out

def getNodeVolume(bounds):
    volume=np.float64(1)
    for i in bounds:
        if np.issubdtype(i.dtype,np.float):
            volume=volume*np.ptp(i)
        elif np.issubdtype(i.dtype,np.integer):
            volume=volume*(np.ptp(i)+1)
    return volume

def getBounds(data):
    """

    :param data:
    :return:
    """
    out_list=[]
    for i in data.columns.values:
        out_list.append(np.array([np.amin(data[i].values),np.amax(data[i].values)]))
    return out_list

if __name__ == "__main__":
    #For Testing Purposes
    print ""

