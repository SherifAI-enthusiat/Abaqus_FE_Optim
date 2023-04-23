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
import ParamTools as par
import os
def fileReader(filePath,cpPath=None):
    dataFile = open(filePath,"r")
    lines = dataFile.readlines()
    dataFile.close()
    if cpPath!=None:
        newmsgfile = open(cpPath,"w")
        for line in lines:
            newmsgfile.writelines(line)
    return lines
cwd = os.getcwd()
paramFile = os.path.join(cwd,"param.ascii") # Test Parameters
lines = fileReader(paramFile)
lst =[]
for line in lines:
    line = line.strip("\n")
    itms=line.split(",")
    for itm in itms:
        lst.append(float(itm))
    test = par.material_stability(lst) and par.transverseIso(lst)
    print(test)