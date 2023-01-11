# from scipy.optimize import least_squares
# from scipy.optimize import minimize
from scipy.io import savemat
import numpy as np
import subprocess,os,sys,shutil
import time
## https://docs.scipy.org/doc/scipy/tutorial/optimize.html#global-optimization
## File paths and variables
# basePath = r'C:\Users\mnsaz\Desktop\ScipyTests'
basePath = os.getcwd()
os.chdir(basePath)
orifile = os.path.join(basePath,"testPinch3.inp")
dataRet = os.path.join(basePath,"dataRetrieval.py")
runDir = os.path.join(basePath,"runDir")
MatlabOutput = os.path.join(basePath,"MatlabOutput")
command = 'abaqus python "%s"'%dataRet
# outputName = os.path.join(basePath,"Outcomes\\feaResults.ascii")
displayScreen = os.path.join(basePath,"Outcomes\\display.ascii")
# expData = np.array([1.07601,0.8989,0.88240,4.10911,4.15046]) ## These are our experimental data -> displacement controlled.
#expData = np.array([0.611925065517,0.631498813629,0.591993808746,0.488072931767,0.738442957401]) ## These are our experimental data -> force controlled.

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
def display(disp_file,fileN=None):
    with open(disp_file,"a") as file:
        for ind,item in enumerate(fileN):
            cm = str(ind) + " %s\n"%item
            file.writelines(cm)

def Abqfunc(x,orifile,workspacePath):
## Function call
    ## Method required to modify Youngs and Poisson
    os.chdir(basePath)
    lines = fileReader(orifile)
    for ind,line in enumerate(lines):
        if line =="*Elastic\n":
            lines[ind+1] = '%s, %s\n'%(x[0],x[1])
    if not os.path.exists(workspacePath):
        os.makedirs(workspacePath)
    workspace = os.path.join(workspacePath,"testPinch3.inp")
    # odbFile = os.path.join(workspacePath,"testPinch2.odb")
    with open(workspace,"w+") as file:
        file.writelines(lines)
    cmd = 'abaqus job=genOdb input="%s" cpus=4'%workspace
    os.chdir(workspacePath)
    pCall = subprocess.call(cmd, shell=True)
    time.sleep(15)
    removefiles(0,workspacePath)
    ## PostProcessing
    if pCall==0:
        # cmd = 'abaqus python %s'%(command)
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

## Run script
# inp1 = 100;inp2 = .3;inp3 = 1  # this is required to test the file without matlab
# workspacePath = runDir + "\workspace_%s"%(inp3)#inp3
# x0 = np.array([inp1,inp2])
## Matlab version
x0 =np.array([sys.argv[-3],sys.argv[-2]]) #
workspacePath = runDir + "\workspace_%s"%(sys.argv[-1])#inp3
data = Abqfunc(x0,orifile,workspacePath)
# try:
#     shutil.rmtree(workspacePath)
# except:
#     pass
