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

def displacementData(datHandle):
    temp = []
    for ind in range(len(datHandle.values)):
        dat = datHandle.values[ind].data
        temp.append(dat)
    return temp

def undeformedCoordData(nodeset,dataPath):
    temp = []
    for ind in range(len(nodeset.nodes[0])):
        point = nodeset.nodes[0][ind].coordinates
        temp.append(point)
    data = np.vstack(temp)
    np.save(dataPath,data)
    return 

def getnodeSet(myOdb,surf):
    for set in myOdb.rootAssembly.nodeSets.keys():
        if set.endswith(surf): # This is either "MEDDisplData" and "LATDisplData"
            subset = myOdb.rootAssembly.nodeSets[set]
            newset = set
    return subset, newset

def RetrieveData():
    odbToolbox = os.path.join(absPath,"postProTools")
    medCoordPath = os.path.join(absPath,"MatlabOutput\medCoordData.npy")
    latCoordPath = os.path.join(absPath,"MatlabOutput\latCoordData.npy")
    medDisplPath = os.path.join(workspacePath,"medDisplData.npy")
    latDisplPath = os.path.join(workspacePath,"latDisplData.npy")
    odbFile = os.path.join(workspacePath,"genOdb_%s.odb"%(workspacePath.split("_")[-1]))
    sys.path.append(odbToolbox)
    # sys.path.append(ContactTool)
    import tools.odbTools as odbTools
    import tools.extractors as ext
    # import OdbTool_1_ver1 as AnOdb_tool
    myOdb = odbTools.openOdb(odbFile)
    
    menSurf =['MEDSURF','LATSURF']
    # Undeformed Coordinates to file - Check to see of the file exists first before writing
    if not os.path.exists(medCoordPath):
        for itm in menSurf:
            subset,set = getnodeSet(myOdb,itm)
            if set.endswith('MEDSURF'):
                undeformedCoordData(subset,medCoordPath)
            else:
                undeformedCoordData(subset,latCoordPath)

    tmp_med = []; tmp_lat =[]
    for _,stpName in enumerate(myOdb.steps.keys()):
        if stpName.startswith('Load'):
            frameData = myOdb.steps[stpName].frames[-1]
            fieldData = frameData.fieldOutputs['U']
            for itm in menSurf:
                subset,surf = getnodeSet(myOdb,itm)
                if surf.endswith('MEDSURF'):
                    dat = fieldData.getSubset(region=subset,position=NODAL)
                    newdat = displacementData(dat)
                    tmp_med.append(newdat)
                else:
                    dat = fieldData.getSubset(region=subset,position=NODAL)
                    newdat = displacementData(dat)
                    tmp_lat.append(newdat)

    for ind in range(2):
        if ind == 0:
            data = np.vstack((tmp_med[0],tmp_med[1],tmp_med[2]))
            np.save(medDisplPath,data)
        else:
            data = np.vstack((tmp_lat[0],tmp_lat[1],tmp_lat[2]))
            np.save(latDisplPath,data)

    myOdb.close()
    return 

RetrieveData()