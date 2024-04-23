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
# stafile = r"D:\Sherif_CT_Download\github\Abaqus_FE_Optim\RunDir\workspace_100\genOdb_100.sta"
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
# workspacePath = r"D:\Sherif_CT_Download\github\Abaqus_FE_Optim\RunDir\workspace_1"
# basePath = os.getcwd()
# staFile = r"D:\Sherif_CT_Download\github\Abaqus_FE_Optim\RunDir\workspace_1\genOdb_1.sta"
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


# #### 
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
# absPath = "D:\Sherif_CT_Download\github\Abaqus_FE_Optim"
# workspacePath = "D:\Sherif_CT_Download\github\Abaqus_FE_Optim\RunDir\workspace_1\genOdb_1.odb"
# OdbqueFile = os.path.join(absPath,"OdbQueue.ascii")
# item2test = fileReader(OdbqueFile)[-1]
# if item2test == workspacePath:
#     test = True
# else:  test = False
# import os, numpy as np
# import subprocess
# import pickle
# workspacePath = "RunDir/workspace_1"
# # outputName = os.path.join(workspacePath,"feaResults.ascii")
# # if os.path.exists(outputName):
# #     dat= np.genfromtxt(outputName, delimiter=",")

## Abaqus version - I use this to read and write results for individual odb files.
# import subprocess,os
import HelperFunc as Hp
workspacePath = "C:\\WorkThings\\github\Abaqus_FE_Optim\\runDir\\workspace_4"
storePath = "Knee 2" # This is to store it to the MatlabOutput folder for evaluation.
pCall2 = Hp.writeOdbResults(workspacePath,storePath)
print(pCall2)


# ## Test script version
# pCall2 = subprocess.Popen(['python',"newScript.py"],stdout=subprocess.PIPE, text=False)
# path = workspacePath + '/data.npy'
# data = np.load(path)
# print(data)
# # output, _ = pCall2.communicate()
# # ## Testing pickle
# # y = pickle.loads(output)
# # print(y)
# # # tmp = pickle.dumps()
# # # print(tmp) 
# import write2InpFile
# import numpy as np
# import os
# basePath =os.getcwd()
# # x0 = np.array([3.5,3.5,3.5,0.2,0.2,0.2,1.4583,1.4583,1.4583]) 
# # orifile = os.path.join(basePath,"TestJob-2.inp")
# workspacePath = "C:\WorkThings\github\Abaqus_FE_Optim\RunDir\workspace_1"
# # workspaceInp = write2InpFile.writeInp(x0,orifile,workspacePath,"TestJob-2.inp")
# latEpiCoordPath = os.path.join(workspacePath,"Results\latEpiCoordData.txt")
# test = os.path.dirname(latEpiCoordPath)

# os.makedirs(latEpiCoordPath)
# kneeName = 'knee 2'
# somVa = 'PC'+ kneeName.replace(' ','')
# print(somVa)
# from HelperFunc import *
# # lines = fileReader("TestJob-2.inp")
# # val = checkInpfile('Knee 4')
# initialise()
# print("Yes")