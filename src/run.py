import argparse
import os, errno
import fnmatch
import time
import pandas as pd
from FRONT.utils.utils import *
from FRONT.Forest.RSForest import *
from FRONT.Forest.NBForest import *

def getlogLiklihood(df):
    df_out=pd.DataFrame()
    df_out.loc[0,'zeros']=len(df[df['score'] == 0])
    df_out.loc[0,'Avg_likelihood']=np.nanmean(np.log(df[df['score'] > 0].values))
    return df_out

def createForest(param):
    df = pd.read_csv(param.in_file)
    if param.type == "RSForest":
        return Forest(1, getBounds(df), param.H, param.M, profileMode=param.profileMode, profileArgs=param.profileArgs, subtree=param.subtree,tree=param.tree)
    elif param.type == "NBForest":
        return NBForest(1, getBounds(df), param.H, param.M, profileMode=param.profileMode, profileArgs=param.profileArgs, subtree=param.subtree,tree=param.tree)

def runPreqRSForest(param):
    total=time.time()
    df = pd.read_csv(param.in_file)
    build=time.time()
    print "building"
    forest=createForest(param)
    build_end=time.time()-build
    print "Scoring"
    if param.eval == "AvgLog":
        score = np.float(0)
        counter=0
        start=time.time()
        for i in range(0, len(df.values)):
            x=df.loc[i, :].values
            t=forest.feed(x)
            #print "Score:", t, " for x: ", x, " At Position: ", i
            if t > 0:
                score += np.log(t)
                counter +=1

        end=time.time()-start

    print "wrapup"
    param.score=score/float(counter)
    param.time_score=end
    param.time_build=build_end
    #print score
    #print end
    #print counter, len(df.values)
    s=str(vars(param))
    #print s
    print "checking dir"
    make_sure_path_exists(param.out_dir)
    print "writing File"
    f=open(param.out_dir+"/"+param.out_file+".txt","w")
    f.write(str(vars(param)))
    f.close()
    print "Total: ",time.time()-total

def runTest(param):
    if param.eval == "AvgLog":
        runPreqRSForest(param)



def searchDir(dirname,filter):
    matches = []
    for root, dirnames, filenames in os.walk(dirname):
        for filename in fnmatch.filter(filenames, filter):
            matches.append(os.path.join(root, filename))

    return matches

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if __name__ == "__main__":
    #Generating the parse argument which carries all parameters needed by the algorithm. NOTE: numpy will create Future/and or runtime warnings, because of recent changes.
    parser=argparse.ArgumentParser(description="FRONT Launcher. NOTE: numpy will create Future/and or runtime warnings, because of recent changes")
    parser.add_argument("-M",action="store",dest="M",type=int,required=True,help="Number of Trees in Forest")
    parser.add_argument("-H", action="store", dest="H",type=int,required=True,help="Depth of each Tree")
    parser.add_argument("-i", action="store", dest="in_file",required=True,help="CSV File with Data")
    parser.add_argument("-o", action="store", dest="out_file",required=False,help="Outfile TXT Name")
    parser.add_argument("-zeta", action="store", dest="zeta",type=float,required=False,default=0.1,help="Node Size Threshold to decide how deep to traverse in each Tree")
    parser.add_argument("-profileMode", action="store", dest="profileMode",default="classic",required=False,help="Which Profile Mode to Use, currently only classic available")
    parser.add_argument("-profileArgs", action="store", dest="profileArgs",default="size=512",required=False,help="Args for Profile Initialisation, effectively the window Size ")
    parser.add_argument("-run", action="store", dest="run", type=int, required=False,default=1,
                        help="Run Number, used to differ outputs for a number of different runs")
    parser.add_argument("-out",action="store",dest="out_dir",required=True,help="Out directory to write the output files to, must exist")
    parser.add_argument("-forest",action="store",dest="type",default="RSForest", type=str,choices=["RSForest","NBForest"],help="Forest Structure Used")
    parser.add_argument("-eval",action="store",dest="eval",default="AvgLog", type=str,choices=["AvgLog"])
    parser.add_argument("-subtree", action="store_true", dest="subtree", default=False, required=False,
                        help="Use subtree volume adjustment")
    parser.add_argument("-tree", action="store", dest="tree", default="RSTree", type=str, choices=["RSTree","NTree"],required=False,
                        help="Tree Structure Used")

    try:
        param=parser.parse_args()
        runTest(param)


    except IOError, msg:
        parser.error(str(msg))