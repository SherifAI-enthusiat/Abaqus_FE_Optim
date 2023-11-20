# from scipy.optimize import least_squares
# from scipy.optimize import minimize
from scipy.io import savemat
import numpy as np
import subprocess,os,sys,shutil
import time
import HelperFunc
# import write2InpFile
## https://docs.scipy.org/doc/scipy/tutorial/optimize.html#global-optimization
## File paths and variables
basePath = os.getcwd()
os.chdir(basePath)
## User Input
inpName = "TestJob-2.inp"
criteriaMod = "*Elastic\n"# "*Elastic, type=ENGINEERING CONSTANTS\n"
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
def display(data,):
    outputName2 = os.path.join(basePath,"debugReport.ascii")
    with open(outputName2,"a") as file:
        if isinstance(data,str):
            file.writelines(data+"\n")
        else:        
            for ind,item in enumerate(data):
                cm = str(ind) + " %s\n"%item
                file.writelines(cm)

## Function call
def Abqfunc(x,orifile,workspacePath):
    ## Method required to modify Youngs and Poisson
    os.chdir(basePath)
    lines = fileReader(orifile)
    for ind,line in enumerate(lines):
        if line =="*Elastic\n":
            param = ",".join(str(t) for i,t in enumerate(x)) + "\n"
            lines[ind+1] = param  #'%s, %s\n'%(x[0],x[1])
    if not os.path.exists(workspacePath):
        os.makedirs(workspacePath)
    workspace = os.path.join(workspacePath,inpName)
    with open(workspace,"w+") as file:
        file.writelines(lines)
    cmd = 'abaqus job=genOdb_%s input="%s" cpus=3'%(Mcount,workspace)
    os.chdir(workspacePath)
    pCall = subprocess.call(cmd, shell=True)
    time.sleep(65)
    removefiles(0,workspacePath)
    ## PostProcessing
    if pCall==0:
        os.chdir(basePath)
        commandn = r'%s -- "%s"'%(command,workspacePath)
        pCall2 = subprocess.call(commandn, shell=True)
        if pCall2==0:
            outputName = os.path.join(workspacePath,"feaResults.ascii")
            dat= np.genfromtxt(outputName, delimiter=",")
            # mdic = {"dat": dat, "label": "experiment"}
            mdic = {"dat": dat}
            output = os.path.join(MatlabOutput,"output_%s.mat"%(Mcount))
            savemat(output, mdic)
            return dat

# ## Run script
# inpArg = 'lstestv2_parallel_v1.py 150 3.250000e-01'
# dictn =[]; tmp1 = inpArg.split(" ")
# for i in range(1,len(tmp1)):
#     tmp ="{:.8f}".format(float(tmp1[i]))
#     dictn.append(tmp)
# x0 =np.hstack([dictn])
# # inp1 = 100;inp2 = .3
# Mcount = 1  # this is required to test the file without matlab
# workspacePath = runDir + "\workspace_%s"%(Mcount)#inp3
# data = Abqfunc(x0,orifile,workspacePath)

# ## Matlab version
dictn =[]
for i in range(1,len(sys.argv)):
    tmp ="{:.8f}".format(float(sys.argv[i]))
    dictn.append(tmp)
x0 =np.hstack([dictn])
wkSpace,Mcount = HelperFunc.communicate()
workspacePath = runDir + "\workspace_%s"%(Mcount)#inp3
data = Abqfunc(x0,orifile,workspacePath)
# try:
#     shutil.rmtree(workspacePath)
# except:
#     pass
