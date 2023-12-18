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
ContactTool = os.path.join(absPath,"Test")
outputFile = os.path.join(workspacePath,"feaResults.ascii")
outputFile2 = os.path.join(workspacePath,"contactResults.ascii")
# genFile = os.path.join(absPath,"feaAll.ascii")
odbFile = os.path.join(workspacePath,"genOdb_%s.odb"%(workspacePath.split("_")[-1]))
sys.path.append(odbToolbox)
sys.path.append(ContactTool)
import tools.odbTools as odbTools
import tools.extractors as ext
import OdbTool_1_ver1 as AnOdb_tool
myOdb = odbTools.openOdb(odbFile)
dictn1=[]; dictn2 = []
for ind,stpName in enumerate(myOdb.steps.keys()):
    if stpName.startswith('Load'):
        try:
            # MenExt = ext.getU_Magnitude(myOdb,"CALIBRATIONNODES",stpName)
            defn = AnOdb_tool.definitions(myOdb,stpName)# Defintions of contact surface areas dictionary
            contVars = AnOdb_tool.answers(defn)
            # dictn1.append([MenExt[-1]])
            dictn2.append([contVars])
        except:
            # dictn1.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            dictn2.append([0, 0, 0, 0, 0, 0])
# display(dictn1)
with open(outputFile2,'a') as datFile_2:
    # tempN1= np.vstack(dictn1); 
    tempN2= np.vstack(dictn2)
    # np.savetxt(datFile_1,tempN1,delimiter=',',fmt='%s')
    np.savetxt(datFile_2,tempN2,delimiter=',',fmt='%s')

myOdb.close()