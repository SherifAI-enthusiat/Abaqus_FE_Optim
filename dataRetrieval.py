import sys,os
import numpy as np
absPath = os.path.dirname(__file__)
workspacePath = sys.argv[-1]
### Display
def display(data):
    outputName2 = os.path.join(absPath,"debugReport.ascii")
    with open(outputName2,"a") as file:
        for ind,item in enumerate(data):
            cm = str(ind) + " %s\n"%item
            file.writelines(cm)
odbToolbox = os.path.join(absPath,"postProTools")
outputFile = os.path.join(workspacePath,"feaResults.ascii")
genFile = os.path.join(absPath,"feaAll.ascii")
odbFile = os.path.join(workspacePath,"genOdb_%s.odb"%(workspacePath.split("_")[-1]))
sys.path.append(odbToolbox)
# sys.path.append(ContactTool)
import tools.odbTools as odbTools
import tools.extractors as ext
# import OdbTool_1_ver1 as AnOdb_tool
myOdb = odbTools.openOdb(odbFile)
dictn1=[]
for ind,stpName in enumerate(myOdb.steps.keys()):
    if stpName.startswith('Load'):
        MenExt = ext.getU_Magnitude(myOdb,"CALIBRATIONNODES",stpName)
        dictn1.append([MenExt[-1]])
# display(dictn1)
with open(outputFile,'a') as datFile_1, open(genFile,'w') as datFile_2:
    tempN1= np.vstack(dictn1); #tempN2= np.vstack(dictn2)
    np.savetxt(datFile_1,tempN1,delimiter=',',fmt='%s')
    np.savetxt(datFile_2,tempN1,delimiter=',',fmt='%s')

myOdb.close()