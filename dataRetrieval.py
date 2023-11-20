import sys,os
import numpy as np
absPath = os.path.dirname(__file__)
workspacePath = sys.argv[-1]

## Added some functions 
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

def fileReader(filePath,cpPath=None):
    dataFile = open(filePath,"r")
    lines = dataFile.readlines()
    dataFile.close()
    if cpPath!=None:
        newmsgfile = open(cpPath,"w")
        for line in lines:
            newmsgfile.writelines(line)
    return lines

def buildfilePath(workspacePath):
    outputFile = os.path.join(workspacePath,"feaResults.ascii")
    # genFile = os.path.join(absPath,"feaAll.ascii")
    odbFile = os.path.join(workspacePath,"genOdb_%s.odb"%(workspacePath.split("_")[-1]))
    return outputFile,odbFile

### Display
def display(data):
    outputName2 = os.path.join(absPath,"debugReport.ascii")
    with open(outputName2,"a") as file:
        for ind,item in enumerate(data):
            cm = str(ind) + " %s\n"%item
            file.writelines(cm)

# To confirm that the workspacePath and what is in the JobQueue are the same.
OdbqueFile = os.path.join(absPath,"OdbQueue.ascii")
item2test = fileReader(OdbqueFile)[-1]
item2test = item2test.strip() # this removes the newline 
item2test = item2test.strip('"')
cmpath = os.path.commonpath([item2test,workspacePath])
st = "workspace_%s"%(workspacePath.split("_")[-1])
if st in cmpath:
    test = True
else:  test = False

odbToolbox = os.path.join(absPath,"postProTools")
sys.path.append(odbToolbox)
# sys.path.append(ContactTool)
import tools.odbTools as odbTools
import tools.extractors as ext
# import OdbTool_1_ver1 as AnOdb_tool

## These are a means to ensure that the instruction that is being run is the desired.
if test:
    paths = buildfilePath(workspacePath)
    myOdb = odbTools.openOdb(paths[-1])
else:
    for item in sys.argv:
        paths = buildfilePath(item2test)
        if paths[-1] in item:
            try:
                myOdb = odbTools.openOdb(paths[-1])
            except:
                display(paths[-1])

## Read and write .odb results
dictn1=[]
for ind,stpName in enumerate(myOdb.steps.keys()):
    if stpName.startswith('Load'):
        MenExt = ext.getU_Magnitude(myOdb,"CALIBRATIONNODES",stpName)
        dictn1.append([MenExt[-1]])
        myOdb.close()
        removefiles(0,workspacePath)
# display(dictn1)
with open(paths[0],'a') as datFile_1:#, open(genFile,'w') as datFile_2:
    tempN1= np.vstack(dictn1); #tempN2= np.vstack(dictn2)
    np.savetxt(datFile_1,tempN1,delimiter=',',fmt='%s')
    # np.savetxt(datFile_2,tempN1,delimiter=',',fmt='%s')
