# from scipy.optimize import least_squares
# from scipy.optimize import minimize
from scipy.io import savemat
import numpy as np
import subprocess,os,sys,shutil
import time, psutil
import pathlib2 as pth
import write2InpFile,HelperFunc
import ParamTools as par
from queue import Queue
## https://docs.scipy.org/doc/scipy/tutorial/optimize.html#global-optimization
## File paths and variables
process_queue = Queue()
basePath =os.getcwd()
os.chdir(basePath)
## User Input
inpName = "TestJob-2.inp"
# criteriaMod = "*Elastic\n"# "*Elastic, type=ENGINEERING CONSTANTS\n"
## Dependancies
orifile = os.path.join(basePath,inpName)
dataRet = os.path.join(basePath,"dataRetrieval.py")
queFile = os.path.join(basePath,"WorkQueue.ascii")
runDir = os.path.join(basePath,"runDir")
MatlabOutput = os.path.join(basePath,"MatlabOutput")
command = 'abaqus python "%s"'%dataRet
## Remove runDir files
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
    if available_memory/1000000 < 10000:
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
        elif tConst==5:
            val = True
        else: val=False
    except:
        val = False
    return val

def ManageQueue(Process,Mcount):
    if Mcount==1:
        fileReader(queFile)[-1]==Mcount
    except: 
    process_queue.put()
    return
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
def communicate():
    ## Build working directory path and variable for matlab
    key =True; count=0
    while key:
        count+=1
        workspacePath = os.path.join(runDir,"workspace_%s"%(count))#inp3
        if not os.path.isdir(workspacePath):
            os.mkdir(workspacePath)
            key=False
    return workspacePath,count

## Function call
def Abqfunc(x,orifile,workspacePath):
    ## Method required to modify Youngs and Poisson
    os.chdir(basePath)
    ## Code to write new .inp file
    workspaceInp = write2InpFile.writeInp(x,orifile,workspacePath,inpName)
    staFile = os.path.join(workspacePath,"genOdb_%s.sta"%(workspacePath.split("_")[-1]))
    cmd = r'abaqus memory=8000mb job=genOdb_%s input="%s" cpus=4'%(workspacePath.split("_")[-1],workspaceInp)
    os.chdir(workspacePath)
    if par.material_stability(x):
        while no_memory():
            time.sleep(156)
        pCall = subprocess.call(cmd,shell=True)
        tConst =0
        while not isCompleted(staFile,tConst):
            time.sleep(180)
            tConst+=1
        removefiles(0,workspacePath)
        ## PostProcessing
        if pCall==0:
            os.chdir(basePath)
            commandn = r'%s -- "%s"'%(command,workspacePath)
            pCall2 = subprocess.call(commandn, shell=True)
            if pCall2==0:
                outputName = os.path.join(workspacePath,"feaResults.ascii")
                dat= np.genfromtxt(outputName, delimiter=",")
                write2matlab(dat,workspacePath)
                return None
    else:
        dat = np.zeros([4,12])
        write2matlab(dat,workspacePath)
## Run script
# x0 = np.array([20,10,50,0.3,0.2,0.2,4.7115,1.4583,1.4583]) # 20,20,100,0.3,0.2,0.2,4.7115,1.4583,1.4583
# inp3 = 1  # this is required to test the file without matlab
# workspacePath = os.path.join(runDir,"workspace_%s"%(inp3))#inp3

## Matlab version
dictn =[]
for i in range(1,len(sys.argv)):
    dictn.append(sys.argv[i])
x0 =np.hstack([dictn])
workspacePath,Mcount=communicate()
data = Abqfunc(x0,orifile,workspacePath)
# try:
#     shutil.rmtree(workspacePath)
# except:
#     pass
