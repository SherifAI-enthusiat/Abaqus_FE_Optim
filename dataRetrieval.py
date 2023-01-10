# This version allows contact pressure along with displacment on nodes to be read
import sys,os
import numpy as np
# ### Display
# outputName2 = os.path.join('C:\Users\mnsaz\Desktop\ScipyTests',"debugReport.ascii")
# def display(disp_file,fileN=None):
#     with open(disp_file,"a") as file:
#         for ind,item in enumerate(fileN):
#             cm = str(ind) + " %s\n"%item
#             file.writelines(cm)
odbToolbox = "C:\Users\mnsaz\Desktop\ScipyTests\postProTools"
# odbName = r"C:\Users\mnsaz\Desktop\ScipyTests\runDir\testPinch1.odb"
workspacePath = sys.argv[-1]
outputFile = os.path.join(workspacePath,"feaResults.ascii")
genFile = r"C:\Users\mnsaz\Desktop\ScipyTests\feaAll.ascii"
odbFile = os.path.join(workspacePath,"testPinch2.odb")
sys.path.append(odbToolbox)
# sys.path.append(ContactTool)
import tools.odbTools as odbTools
import tools.extractors as ext
# import OdbTool_1_ver1 as AnOdb_tool
myOdb = odbTools.openOdb(odbFile)
dictn1=[]
# displExt = ext.getU_Magnitude(myOdb,"CALIBRATION_SET",stepName)
# MenExt = ext.getU_Magnitude(myOdb,"CALIBRATION_SET_MEN",stepName)
MenExt = ext.getU_Magnitude(myOdb,"CALIBRATIONNODES")
# temp = [Labels[i-1],a,b]
# temp = str(temp)+"\n"
dictn1.append([MenExt[-1]])
# ar = np.array([sys.argv[-2],sys.argv[-1]])
with open(outputFile,'a') as datFile_1, open(genFile,'a') as datFile_2:
    tempN1= np.vstack(dictn1); #tempN2= np.vstack(dictn2)
    np.savetxt(datFile_1,tempN1,delimiter=',',fmt='%s')
    np.savetxt(datFile_2,tempN1,delimiter=',',fmt='%s')

myOdb.close()