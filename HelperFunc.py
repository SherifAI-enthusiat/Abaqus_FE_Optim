import os,sys
import glob
import psutil, shutil
from scipy.io import savemat
import numpy as np
from queue import Queue

## Paths
process_queue = Queue(maxsize=1)
basePath =os.getcwd()
os.chdir(basePath)
MatlabOutput = os.path.join(basePath,"MatlabOutput")
queFile = os.path.join(basePath,"WorkQueue.ascii")
runDir = os.path.join(basePath,"runDir")

def write2File(outFile,dictn1):
    with open(outFile,'a') as datFile_1:
        tempN1= np.array([dictn1]); #tempN2= np.vstack(dictn2)
        np.savetxt(datFile_1,tempN1,delimiter=',',fmt='%s')
    return 

def removefiles(mode,path=None):
    os.chdir(path)
    files = os.listdir()
    if mode==1: ## mode can be zero or one 
        for file in files:
            os.remove(file)
    else:
        for file in files:
            if file.endswith(".lck"):
                os.remove(file)
def no_memory():
    virtual_memory = psutil.virtual_memory()
    available_memory = virtual_memory.available
    if available_memory/1000000 < 20000:
        val = True
    else:val = False
    return val

### File read
def fileReader(filePath,cpPath=None):
    dataFile = open(filePath,"r")
    lines = dataFile.readlines()
    dataFile.close()
    if cpPath!=None:
        newmsgfile = open(cpPath,"w")
        for line in lines:
            newmsgfile.writelines(line)
    return lines

## Check solution has finished
def isCompleted(staFile,tConst):
    try:
        if fileReader(staFile)[-1] == " THE ANALYSIS HAS COMPLETED SUCCESSFULLY\n":
            val = True
        elif tConst==50 or fileReader(staFile)[-1] ==" THE ANALYSIS HAS NOT BEEN COMPLETED\n":
            val = True
        else: val=False
    except:
        val = False
    return val

def ManageQueue(Process,Mcount,check):
    if Mcount==1:
        write2File(queFile,Mcount)
        process_queue.put(Process)
        check = False
    else:
        if int(fileReader(queFile)[-1])+1==Mcount:
            write2File(queFile,Mcount)
            process_queue.put(Process)
            check = False
    return process_queue,check
### Write to .mat file
def write2matlab(dat,workspacePath):
    mdic = {"dat": dat, "label": "experiment"}
    output = os.path.join(MatlabOutput,"output_%s.mat"%(workspacePath.split("_")[-1]))
    savemat(output, mdic)  
    return 

### Display
def display(data):
    outputName2 = os.path.join(basePath,"debugReport.ascii")
    with open(outputName2,"a") as file:
        for ind,item in enumerate(data):
            cm = str(ind) + " %s\n"%item
            file.writelines(cm)

## Build working directory path and variable for matlab
def communicate():
    key =True; count=0
    while key:
        count+=1
        workspacePath = os.path.join(runDir,"workspace_%s"%(count))#inp3
        if not os.path.isdir(workspacePath):
            os.mkdir(workspacePath)
            key=False
    return workspacePath,count

## The aim of this function is to check and ensure everything is in order before starting the optimisation
# This includes deleting workspace_%d folders, clearing out WorkQueue.ascii file.
def initialise():
    workspacePaths = glob.glob(os.path.join(runDir,"workspace_*"))#inp3
    output = glob.glob(os.path.join(MatlabOutput,"output_*.mat"))
    queFile = [os.path.join(basePath,"WorkQueue.ascii")]
    files2delete = workspacePaths + output + queFile
    for path in files2delete:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            pass
    return
