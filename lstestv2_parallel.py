# from scipy.optimize import least_squares
# from scipy.optimize import minimize
from scipy.io import savemat
import numpy as np
import subprocess,os,sys
import time, psutil
import pathlib2 as pth
import write2InpFile
import HelperFunc
import ParamTools as par
from queue import Queue
## https://docs.scipy.org/doc/scipy/tutorial/optimize.html#global-optimization
## File paths and variables
process_queue = Queue(maxsize=1)
basePath =os.getcwd()
os.chdir(basePath)
## User Input
inpName = "TestJob-2.inp"
# criteriaMod = "*Elastic\n"# "*Elastic, type=ENGINEERING CONSTANTS\n"
## Dependancies
orifile = os.path.join(basePath,inpName)
dataRet = os.path.join(basePath,"dataRetrieval.py")
command = 'abaqus python "%s"'%dataRet

## Function call
def Abqfunc(x,orifile,workspacePath):
    ## Method required to modify Youngs and Poisson
    os.chdir(basePath)
    check = True; tConst =0
    ## Code to write new .inp file
    workspaceInp = write2InpFile.writeInp(x,orifile,workspacePath,inpName)
    jobName = "genOdb_%s"%(workspacePath.split("_")[-1])
    staFile = os.path.join(workspacePath,"genOdb_%s.sta"%(workspacePath.split("_")[-1]))
    os.chdir(workspacePath)
    if par.material_stability(x) and check:
        cmd = r'abaqus memory=20000mb job=genOdb_%s input="%s" cpus=4'%(workspacePath.split("_")[-1],workspaceInp)
        while check:
            process_queue, check = HelperFunc.ManageQueue(cmd,Mcount,check)
        while not process_queue.empty():
            while HelperFunc.no_memory():
                time.sleep(156)
            process = process_queue.get()
            pro = subprocess.Popen(process,stdout=subprocess.PIPE,shell=True,
                             creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        while not HelperFunc.isCompleted(staFile,tConst)[0]:
            time.sleep(60)
            tConst+=1
        if HelperFunc.isCompleted(staFile,tConst)[1]:
            HelperFunc.kill_proc(jobName)
        HelperFunc.removefiles(0,workspacePath)
        ## PostProcessing
    dat = np.zeros([4,12])
    if check== False and HelperFunc.fileReader(staFile)[-1] == " THE ANALYSIS HAS COMPLETED SUCCESSFULLY\n":
            os.chdir(basePath)
            commandn = r'%s -- "%s"'%(command,workspacePath)
            pCall2 = subprocess.call(commandn, shell=True)
            if pCall2==0:
                outputName = os.path.join(workspacePath,"feaResults.ascii")
                dat= np.genfromtxt(outputName, delimiter=",")
                HelperFunc.write2matlab(dat,workspacePath)
            else:
                HelperFunc.write2matlab(dat,workspacePath)
    else:
        HelperFunc.write2matlab(dat,workspacePath)
# ## Run script
# x0 = np.array([6.673, 6.673, 229.25, 0.01, 0.01, 0.01, 3.304, 12.6,12.6]) # {6.673, 6.673, 229.25, 0.01, 0.01, 0.01, 3.304, 12.6,12.6 } Breaks
# inp3 = 1
# Mcount = 1  # this is required to test the file without matlab
# runDir = os.path.join(basePath,"runDir")
# workspacePath = os.path.join(runDir,"workspace_%s"%(inp3))#inp3
# data = Abqfunc(x0,orifile,workspacePath)

## Matlab version
dictn =[]
for i in range(1,len(sys.argv)):
    dictn.append(sys.argv[i])
x0 =np.hstack([dictn])
workspacePath,Mcount=HelperFunc.communicate()
data = Abqfunc(x0,orifile,workspacePath)
# try:
#     shutil.rmtree(workspacePath)
# except:
#     pass
