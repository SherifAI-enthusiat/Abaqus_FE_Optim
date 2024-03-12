import sys,os
import numpy as np
absPath = os.path.dirname(__file__)
tmp = sys.argv[-1].split("-")
workspacePath = tmp[0]
storePath = tmp[-1]
from odbAccess import NODAL
### Display
def display(data):
    outputName2 = os.path.join(absPath,"debugReport.ascii")
    with open(outputName2,"a") as file:
        if type(data)==list:
            for ind,item in enumerate(data):
                cm = str(ind) + " %s\n"%item
                file.writelines(cm)
        else:
            file.writelines(data)

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
    np.savetxt(dataPath,data,delimiter=",")
    return 

def saveData2File(filePath,tmp,append=False):
    if append ==True:
        data = np.vstack((tmp[0][0],tmp[1][0],tmp[2][0],tmp[3][0]))
        with open(filePath,'a') as filePath:
            np.savetxt(filePath,data,delimiter=',')
    else:
        data = np.vstack((tmp[0],tmp[1],tmp[2],tmp[3]))
        np.savetxt(filePath,data,delimiter=',')
    return

def getnodeSet(myOdb,surf):
    for set in myOdb.rootAssembly.nodeSets.keys():
        if set.endswith(surf): # This is either "MEDDisplData" and "LATDisplData"
            subsetHandle = myOdb.rootAssembly.nodeSets[set]
            newset = set
    return subsetHandle, newset

def RetrieveData():
    odbToolbox = os.path.join(absPath,"postProTools")
    medCoordPath = os.path.join(absPath,"%s\medCoordData.txt"%(storePath))
    latCoordPath = os.path.join(absPath,"%s\latCoordData.txt"%(storePath))
    medEpiCoordPath = os.path.join(workspacePath,"Results\medEpiCoordData.txt")
    latEpiCoordPath = os.path.join(workspacePath,"Results\latEpiCoordData.txt")
    medDisplPath = os.path.join(workspacePath,"Results\medDisplData.txt")
    latDisplPath = os.path.join(workspacePath,"Results\latDisplData.txt")
    odbFile = os.path.join(workspacePath,"genOdb_%s.odb"%(workspacePath.split("_")[-1]))
    os.mkdir(os.path.dirname(latEpiCoordPath)) # Creates the Results path for my files
    sys.path.append(odbToolbox)
    # sys.path.append(ContactTool)
    import tools.odbTools as odbTools
    import tools.extractors as ext
    # import OdbTool_1_ver1 as AnOdb_tool
    myOdb = odbTools.openOdb(odbFile)
    
    menSurf = ['MEDSURF','LATSURF']
    epiCoords = ['MEDEPICONDYLE','LATEPICONDYLE']
    # Undeformed Coordinates to file - Check to see of the file exists first before writing
    if not os.path.exists(medCoordPath):
        for itm in menSurf:
            subsetHandle,set = getnodeSet(myOdb,itm)
            if set.endswith('MEDSURF'):
                undeformedCoordData(subsetHandle,medCoordPath)
            elif set.endswith('LATSURF'):
                undeformedCoordData(subsetHandle,latCoordPath)

    for itm in epiCoords:
        subsetHandle,set = getnodeSet(myOdb,itm)
        if set.endswith('MEDEPICONDYLE'):
            undeformedCoordData(subsetHandle,medEpiCoordPath)
        elif set.endswith('LATEPICONDYLE'):
            undeformedCoordData(subsetHandle,latEpiCoordPath)

    menSurfn = ['MEDSURF','LATSURF','MEDEPICONDYLE','LATEPICONDYLE']
    tmp_med = []; tmp_lat =[]; tmp_epi_med =[];tmp_epi_lat =[]
    for _,stpName in enumerate(myOdb.steps.keys()):
        if stpName.startswith('Load') or stpName.startswith('Move'):
            frameData = myOdb.steps[stpName].frames[-1]
            fieldData = frameData.fieldOutputs['U']
            for itm in menSurfn:
                subsetHandle,surf = getnodeSet(myOdb,itm)
                if surf.endswith('MEDSURF'):
                    dat = fieldData.getSubset(region=subsetHandle,position=NODAL)
                    newdat = displacementData(dat)
                    tmp_med.append(newdat)
                elif surf.endswith('LATSURF'):
                    dat = fieldData.getSubset(region=subsetHandle,position=NODAL)
                    newdat = displacementData(dat)
                    tmp_lat.append(newdat)
                elif surf.endswith('MEDEPICONDYLE'):
                    dat = fieldData.getSubset(region=subsetHandle,position=NODAL)
                    newdat = displacementData(dat)
                    tmp_epi_med.append(newdat)
                elif surf.endswith('LATEPICONDYLE'):
                    dat = fieldData.getSubset(region=subsetHandle,position=NODAL)
                    newdat = displacementData(dat)
                    tmp_epi_lat.append(newdat)

    # Saving files to folder.
    saveData2File(medDisplPath,tmp_med)
    saveData2File(latDisplPath,tmp_lat)
    saveData2File(medEpiCoordPath,tmp_epi_med,append=True)
    saveData2File(latEpiCoordPath,tmp_epi_lat,append=True)

    myOdb.close()
    return 
# tmpn = sys.argv[-1].split("-")
# tmp = "StorePath Path: %s\n"%(tmpn[-1])
# tmp1 = "WorkspacePath Path: %s\n"%(tmpn[0])
# display(tmp)
# display(tmp1)
RetrieveData()