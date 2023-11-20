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
# cwd = os.getcwd()
# paramFile = os.path.join(cwd,"param.ascii") # Test Parameters
# lines = fileReader(paramFile)
# lst =[]
# for line in lines:
#     line = line.strip("\n")
#     itms=line.split(",")
#     for itm in itms:
#         lst.append(float(itm))
#     test = par.material_stability(lst) and par.transverseIso(lst)
#     print(test)

from scipy.io import savemat
import numpy as np
import os
def testMat():
    workspacePath = "D:\Sherif_CT_Download\github\Abaqus_FE_Optim\runDir\workspace_2\feaResults.ascii"
    # outputName = os.path.join(workspacePath,"feaResults.ascii")
    dat= np.genfromtxt(workspacePath, delimiter=",")
    # mdic = {"dat": dat, "label": "experiment"}
    mdic = {"dat": dat}
    # output = os.path.join(MatlabOutput,"output_%s.mat"%(Mcount))
    # savemat(output, mdic)
    return mdic