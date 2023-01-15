# from scipy.optimize import least_squares
# from scipy.optimize import minimize
from scipy.io import savemat
import numpy as np
import subprocess,os,sys,shutil
import time
import write2InpFile
import ParamTools as par
## https://docs.scipy.org/doc/scipy/tutorial/optimize.html#global-optimization
## File paths and variables
basePath = os.getcwd()
os.chdir(basePath)
## User Input
inpName = "TestJob-2.inp"
# criteriaMod = "*Elastic\n"# "*Elastic, type=ENGINEERING CONSTANTS\n"
## Dependancies
orifile = os.path.join(basePath,inpName)
dataRet = os.path.join(basePath,"dataRetrieval.py")
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

### Display
def display(data):
    outputName2 = os.path.join(basePath,"debugReport.ascii")
    with open(outputName2,"a") as file:
        for ind,item in enumerate(data):
            cm = str(ind) + " %s\n"%item
            file.writelines(cm)

## Function call
def Abqfunc(x,orifile,workspacePath):
    ## Method required to modify Youngs and Poisson
    os.chdir(basePath)
    ## Code to write new .inp file
    workspaceInp = write2InpFile.writeInp(x,orifile,workspacePath,inpName)
    cmd = 'abaqus job=genOdb input="%s" cpus=4'%workspaceInp
    os.chdir(workspacePath)
    if par.material_stability(x):
        pCall = subprocess.call(cmd,shell=True)
        time.sleep(780)
        removefiles(0,workspacePath)
        ## PostProcessing
        if pCall==0:
            os.chdir(basePath)
            commandn = r'%s -- "%s"'%(command,workspacePath)
            pCall2 = subprocess.call(commandn, shell=True)
            if pCall2==0:
                outputName = os.path.join(workspacePath,"feaResults.ascii")
                dat= np.genfromtxt(outputName, delimiter=",")
                mdic = {"dat": dat, "label": "experiment"}
                output = os.path.join(MatlabOutput,"output_%s.mat"%(workspacePath.split("_")[-1]))
                savemat(output, mdic)
                return None
    else:
        dat = np.zeros([4,12])
        mdic = {"dat": dat, "label": "experiment"}
        output = os.path.join(MatlabOutput,"output_%s.mat"%(workspacePath.split("_")[-1]))
        savemat(output, mdic)        

## Run script
# inp = np.array([20,20,100,0.3,0.2,0.2,4.7115,1.4583,1.4583])
# inp3 = 1  # this is required to test the file without matlab
# workspacePath = runDir + "\workspace_%s"%(inp3)#inp3
# x0 = inp
## Matlab version
dictn =[]
for i in range(1,len(sys.argv)-1):
    dictn.append(sys.argv[i])
x0 =np.hstack([dictn])
# workspacePath = runDir + "\workspace_%s"%(sys.argv[-1])#inp3
workspacePath = os.path.join(runDir,"workspace_%s"%(sys.argv[-1]))#inp3
data = Abqfunc(x0,orifile,workspacePath)
# try:
#     shutil.rmtree(workspacePath)
# except:
#     pass
