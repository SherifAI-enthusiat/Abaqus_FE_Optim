# import psutil

# def no_memory():
#     virtual_memory = psutil.virtual_memory()
#     available_memory = virtual_memory.available
#     if available_memory/1000000 < 8800:
#         val = True
#     else:val = False
#     return val

# print(no_memory())

### Test a given list of material parameters to see if they are transverse isotropic
# import ParamTools as par
# import os
# def fileReader(filePath,cpPath=None):
#     dataFile = open(filePath,"r")
#     lines = dataFile.readlines()
#     dataFile.close()
#     if cpPath!=None:
#         newmsgfile = open(cpPath,"w")
#         for line in lines:
#             newmsgfile.writelines(line)
#     return lines
# # paramFile = os.path.join(cwd,"param.ascii") # Test Parameters
# lines = fileReader(paramFile)
# lst =[]
# for line in lines:
#     line = line.strip("\n")
#     itms=line.split(",")
#     for itm in itms:
#         lst.append(float(itm))
#     test = par.material_stability(lst) and par.transverseIso(lst)
#     print(test)

## Test to determine if stafile is the reason for failure to read results
# stafile = r"D:\Sherif_CT_Download\github\Abaqus_FE_Optim\runDir\workspace_100\genOdb_100.sta"
# basePath = r"D:\Sherif_CT_Download\github\Abaqus_FE_Optim"
# while not os.path.exists(stafile):
#     print("Works")
# if fileReader(stafile)[-1] == " THE ANALYSIS HAS COMPLETED SUCCESSFULLY\n":
#     dataRet = os.path.join(basePath,"dataRetrieval.py")
#     command = 'abaqus python "%s"'%dataRet
# co =0
# for it in range(6):
#     co+=co
#     print(co)
# import HelperFunc
# import subprocess
# import time
# import numpy as np
# workspacePath = r"D:\Sherif_CT_Download\github\Abaqus_FE_Optim\runDir\workspace_1"
# basePath = os.getcwd()
# staFile = r"D:\Sherif_CT_Download\github\Abaqus_FE_Optim\runDir\workspace_1\genOdb_1.sta"
# dataRet = os.path.join(basePath,"dataRetrieval.py")
# command = 'abaqus python "%s"'%dataRet
# dat = np.zeros([4,12])
# if HelperFunc.fileReader(staFile)[-1] == " THE ANALYSIS HAS COMPLETED SUCCESSFULLY\n":
#         os.chdir(basePath); count =0
#         outputName = os.path.join(workspacePath,"feaResults.ascii")
#         commandn = r'%s -- "%s"'%(command,workspacePath)
#         while not os.path.exists(outputName) and count<=8:
#             pro = subprocess.Popen(commandn,stdout=subprocess.PIPE,shell=True,
#                              creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
#             if not os.path.exists(outputName):
#                 time.sleep(60)
#                 count += 1
#         try:
#             dat= np.genfromtxt(outputName, delimiter=",")
#             HelperFunc.write2matlab(dat,workspacePath)
#         except:
#             HelperFunc.write2matlab(dat,workspacePath)
# else:
#     HelperFunc.write2matlab(dat,workspacePath)

### 
# from queue import Queue
# output_queue = Queue(maxsize=1)
# parent_pid = 0
# ##
# if HelperFunc.fileReader(staFile)[-1] == " THE ANALYSIS HAS COMPLETED SUCCESSFULLY\n":
#         os.chdir(basePath); count =0
#         output_queue = Queue(maxsize=1)
#         outputName = os.path.join(workspacePath,"feaResults.ascii")
#         commandn = r'%s -- "%s"'%(command,workspacePath)
#         dir2 = os.path.split(outputName)
#         output_queue.put(commandn)
#         while not output_queue.empty():
#             while not os.path.exists(outputName) and workspacePath==dir2[0] and count<=8:
#                 process = output_queue.get()
#                 pro = subprocess.Popen(process,stdout=subprocess.PIPE,shell=True,
#                                     creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
#                 if not os.path.exists(outputName):
#                     time.sleep(60)
#                     count += 1
#             try:
#                 dat= np.genfromtxt(outputName, delimiter=",")
#                 HelperFunc.write2matlab(dat,workspacePath)
#             except:
#                 HelperFunc.write2matlab(dat,workspacePath)
# else:
#     HelperFunc.write2matlab(dat,workspacePath)


#### 
import os,glob
import numpy as np
def fileReader(filePath,cpPath=None):
    dataFile = open(filePath,"r")
    lines = dataFile.readlines()
    dataFile.close()
    if cpPath!=None:
        newmsgfile = open(cpPath,"w")
        for line in lines:
            newmsgfile.writelines(line)
    return lines
# absPath = "D:\Sherif_CT_Download\github\Abaqus_FE_Optim"
# workspacePath = "D:\Sherif_CT_Download\github\Abaqus_FE_Optim\runDir\workspace_1\genOdb_1.odb"
# OdbqueFile = os.path.join(absPath,"OdbQueue.ascii")
# item2test = fileReader(OdbqueFile)[-1]
# if item2test == workspacePath:
#     test = True
# else:  test = False
resultsFile = "AllResults.ascii"
test = glob.glob("runDir\workspace_*")
data = []
for ind,itm in enumerate(test):
    path1 = os.path.join(itm,'TestJob-2.inp'); 
    path2 = os.path.join(itm,'feaResults.ascii'); 
    dat= np.genfromtxt(path2, delimiter=",")
    lines = fileReader(path1)
    for ind,itm in enumerate(lines):
        if itm.startswith('*Material') and itm.endswith('name=MENISCAL_MEN\n'):
            tt = np.array([lines[ind+2].strip("\n")])
            new = np.hstack([tt,dat[-1]])
            data.append(new)
         
with open(resultsFile,"a+") as datFile:
    datFile.writelines(data)
