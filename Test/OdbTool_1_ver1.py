from odbAccess import *
from abaqusConstants import *
import inspect, os
import csv
### SMZ -->(19/11/2021)This is an adaptation of OdbTool_1_ver1 to allow me to collect knee CP and CA

# Define step and frame
def definitions(myOdb,stepName="load",csvName=None):
    # stepName = "load"
    step = myOdb.steps[stepName]
    lastFrame = step.frames[-1]
    var ={} # A disctionary to store things in
    # The aim is to calculate the mean comtact pressure on the medial and lateral tibial compartments
    # Look for contact mechanics at medial tibial cartilage due to contact with medial meniscus
    CP_MED_MEN = "CPRESS   ASSEMBLY_SF_MEDIAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_MED_SELF_CONTACT"
    var["CMMvalues"] = lastFrame.fieldOutputs[CP_MED_MEN].values
    CA_MED_MEN = "CNAREA   ASSEMBLY_SF_MEDIAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_MED_SELF_CONTACT"
    var["AMMvalues"] = lastFrame.fieldOutputs[CA_MED_MEN].values
    CF_MED_MEN = "CNORMF   ASSEMBLY_SF_MEDIAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_MED_SELF_CONTACT"
    var["FMMvalues"] = lastFrame.fieldOutputs[CF_MED_MEN].values
    # var["MM"] = [CMMvalues,AMMvalues,FMMvalues]

    # Look for comtact mechanics at medial tibial cartilage due to contact with femoral cartilage
    CP_MED_TIB = "CPRESS   ASSEMBLY_SF_TCART_MED_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
    var["CMTvalues"] = lastFrame.fieldOutputs[CP_MED_TIB].values
    CA_MED_TIB = "CNAREA   ASSEMBLY_SF_TCART_MED_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
    var["AMTvalues"] = lastFrame.fieldOutputs[CA_MED_TIB].values
    CF_MED_TIB = "CNORMF   ASSEMBLY_SF_TCART_MED_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
    var["FMTvalues"] = lastFrame.fieldOutputs[CF_MED_TIB].values
    # var["MT"] = [CMTvalues,AMTvalues,FMTvalues]
    # Look for comtact mechanics at lateral tibial cartilage due to contact with lateral meniscus
    CP_LAT_MEN = "CPRESS   ASSEMBLY_SF_LATERAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_LAT_SELF_CONTACT"
    var["CLMvalues"] = lastFrame.fieldOutputs[CP_LAT_MEN].values
    CA_LAT_MEN = "CNAREA   ASSEMBLY_SF_LATERAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_LAT_SELF_CONTACT"
    var["ALMvalues"] = lastFrame.fieldOutputs[CA_LAT_MEN].values
    CF_LAT_MEN = "CNORMF   ASSEMBLY_SF_LATERAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_LAT_SELF_CONTACT"
    var["FLMvalues"] = lastFrame.fieldOutputs[CF_LAT_MEN].values
    # var["LM"] = [CLMvalues,ALMvalues,FLMvalues]

    # Look for comtact mechanics at lateral tibial cartilage due to contact with femoral cartilage
    CP_LAT_TIB = "CPRESS   ASSEMBLY_SF_TCART_LAT_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
    var["CLTvalues"] = lastFrame.fieldOutputs[CP_LAT_TIB].values
    CA_LAT_TIB = "CNAREA   ASSEMBLY_SF_TCART_LAT_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
    var["ALTvalues"] = lastFrame.fieldOutputs[CA_LAT_TIB].values
    CF_LAT_TIB = "CNORMF   ASSEMBLY_SF_TCART_LAT_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
    var["FLTvalues"] = lastFrame.fieldOutputs[CF_LAT_TIB].values
    # var["LT"] = [CLTvalues,ALTvalues,FLTvalues]

    # Create csv file to record output measures
    if csvName!=None:
        csvName +='.csv'
        try:
            Res = open(csvName, 'a') 
        except:
            Res = open(csvName, 'w')
        Res.write('Location,TotalCNORMF,TotalForce,TotalArea,MeanCP\n')
        Res.close()
    return var

# This function outputs all the node label and requested field output in a separate file
# For double checking anything if needed
def detailcheck(Cvalue, Avalue, Fvalue):
    csvCheck = 'Check.csv'
    Check = open (csvCheck, 'w')
    for i in range (0,len(Cvalue)):
        # if Fvalue[i].magnitude != 0:
        Check.write('%d,%.4f,%.4f,%.4f,%.4f\n'
            %(Cvalue[i].nodeLabel,Cvalue[i].data,Avalue[i].data,Fvalue[i].magnitude,Fvalue[i].data[2]))
    Check.close()
    return

def findcp(Fvalue, Cvalue, Avalue, Loca,csvName=None):
    n = len(Cvalue)
    # Abaqus field output gives the output on one surface first, then the other surface
    # The aim here is to find the break point that separates the two surfaces in the contact pair
    bk = 0
    detailcheck(Cvalue,Avalue,Fvalue)
    # while Cvalue[bk+1].nodeLabel>Cvalue[bk].nodeLabel:
    while -1*Fvalue[bk+1].data[2]<=0:
        bk += 1
    #print 'Break point here is: ' + str(bk)    
        # Here to calculate the outputs of interest on surface 1
    Location1 = Loca.split('.')[0]
    Tcf1 = 0
    TF1 = 0
    TA1 = 0
    MCP1 = 0
    for i in range(0,bk+1):
        Tcf1 += Fvalue[i].magnitude
        TF1 += Cvalue[i].data * Avalue[i].data
        TA1 += Avalue[i].data
    if TA1 != 0:
        MCP1 = TF1/TA1
    
    # Here to calculate the outputs of interest on surface 2
    Location2 = Loca.split('.')[1]
    Tcf2 = 0
    TF2 = 0
    TA2 = 0
    MCP2 = 0
    for i in range(bk+1,n):
        Tcf2 += Fvalue[i].magnitude
        TF2 += Cvalue[i].data * Avalue[i].data
        TA2 += Avalue[i].data
    if TA2 != 0:
        MCP2 = TF2/TA2
    
    # To write down the contact mechanics on each individual contact surface in each contact pair 
    if csvName!=None:
        csvName +='.csv'
        with open(csvName, 'a') as csvfile:
            csvfile.write('%s,%.4f,%.4f,%.4f,%.4f\n'%(Location1, Tcf1, TF1, TA1, MCP1))
            csvfile.write('%s,%.4f,%.4f,%.4f,%.4f\n'%(Location2, Tcf2, TF2, TA2, MCP2))
    
    # Return the total calculated force and total area, for later use
    var={"Loca1":[Location1, Tcf1, TF1, TA1, MCP1],"Loca2":[Location2, Tcf2, TF2, TA2, MCP2]}
    return var, TF1, TA1, TF2, TA2


# Here to analyse the contact mechanics in the four contact pairs
# First letter, m for medial, l for lateral
# Second letter, m for meniscus, t for tibia
# FC is always femoral cartilage
def answers(dictn,csvName=None):
    MMct = findcp(dictn["FMMvalues"], dictn["CMMvalues"], dictn["AMMvalues"], 'MM.MT',csvName) # " ASSEMBLY_SF_MEDIAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_MED_SELF_CONTACT"
    MTct = findcp(dictn["FMTvalues"], dictn["CMTvalues"], dictn["AMTvalues"], 'MT.FC',csvName) # " ASSEMBLY_SF_TCART_MED_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
    LMct = findcp(dictn["FLMvalues"], dictn["CLMvalues"], dictn["ALMvalues"], 'LM.LT',csvName) # " ASSEMBLY_SF_LATERAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_LAT_SELF_CONTACT"
    LTct = findcp(dictn["FLTvalues"], dictn["CLTvalues"], dictn["ALTvalues"], 'LT.FC',csvName) # " ASSEMBLY_SF_TCART_LAT_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"

    # Here to calculate the mean contact pressure on each of the tibial compartments
    # The force is the sum of (tibia contact force due to meniscus + due to femoral cartilage)
    # The area is the sum of (tibia contact area due to meniscus + due to femoral cartilage)
    MedialCP = 0
    LateralCP = 0
    if MMct[4]+MTct[2] != 0:
        MCF = MMct[3]+MTct[1] # Medial contact force
        MCA = MMct[4]+MTct[2] # Medial contact area
        MedialCP = MCF/MCA
    if LMct[4]+LTct[2] != 0 :
        LCF = LMct[3]+LTct[1] # Lateral contact force
        LCA = LMct[4]+LTct[2] # Lateral contact area
        LateralCP = LCF/LCA
    if csvName!=None:
        csvName +='.csv'
        with open(csvName, 'a') as csvfile:
            csvfile.write('\nMean contact pressure at medial tibia: ' + str(MedialCP))
            csvfile.write('\nMean contact pressure at lateral tibia: ' + str(LateralCP))
    return MedialCP, MCF,MCA,LateralCP,LCF,LCA


# # This function calculates the mean cpressure using field force/field area
# def Fctfa():
#     FMM = 0
#     AMM = 0
#     for i in range (0,len(FMMvalues)):
#         FMM += FMMvalues[i].magnitude
#         AMM += AMMvalues[i].data
#         i += 1
#     FMT = 0
#     AMT = 0
#     for i in range (0,len(FMTvalues)):
#         FMT += FMTvalues[i].magnitude
#         AMT += AMTvalues[i].data
#         i += 1
#     FLM = 0
#     ALM = 0
    
#     for i in range (0,len(FLMvalues)):
#         FLM += FLMvalues[i].magnitude
#         ALM += ALMvalues[i].data
#         i += 1
#     FLT = 0
#     ALT = 0
#     for i in range (0,len(FLTvalues)):
#         FLT += FLTvalues[i].magnitude
#         ALT += ALTvalues[i].data
#         i += 1
        
#     mct_med = (FMM+FMT)/(AMM+AMT)
#     mct_lat = (FLM+FLT)/(ALM+ALT)
#     print 'Medial loading: ' + str(FMM+FMT) + ' over ' + str(AMM+AMT)
#     print 'Lateral loading: ' + str(FLM+FLT) + ' over ' + str(ALM+ALT)
#     print 'Using field force over field area, cp med: ' + str(mct_med)
#     print 'Using field force over field area, cp lat: ' + str(mct_lat)
#     print
#     return
# #Fctfa()


# # This function calculates the mean cpressure using field sum nodal(pressure*area)/total field area
# def Fctpres():
#     sigCMMF = 0
#     sigCMMA = 0
#     for i in range(0,len(CMMvalues)):
#             sigCMMF += CMMvalues[i].data * AMMvalues[i].data
#             sigCMMA += AMMvalues[i].data
            
#     sigCMTF = 0
#     sigCMTA = 0
#     for i in range(0,len(CMTvalues)):
#             sigCMTF += CMTvalues[i].data * AMTvalues[i].data
#             sigCMTA += AMTvalues[i].data
            
#     sigCLMF = 0
#     sigCLMA = 0
#     for i in range(0,len(CLMvalues)):
#             sigCLMF += CLMvalues[i].data * ALMvalues[i].data
#             sigCLMA += ALMvalues[i].data
            
#     sigCLTF = 0
#     sigCLTA = 0
#     for i in range(0,len(CLTvalues)):
#             sigCLTF += CLTvalues[i].data * ALTvalues[i].data
#             sigCLTA += ALTvalues[i].data
              
#     meanCP_medial = (sigCMMF+sigCMTF)/(sigCMMA+sigCMTA)
#     meanCP_lateral = (sigCLMF+sigCLTF)/(sigCLMA+sigCLTA)
#     print 'Medial loading: ' + str(sigCMMF+sigCMTF) + ' over ' + str(sigCMMA+sigCMTA)
#     print 'Lateral loading: ' + str(sigCLMF+sigCLTF) + ' over ' + str(sigCLMA+sigCLTA)
#     print 'Using nodal PA over sigma area, cp med: ' + str(meanCP_medial)
#     print 'Using nodal PA over sigma area, cp lat: ' + str(meanCP_lateral)
#     print
#     return
# #Fctpres()


# # The above two added up the values in the two surfaces in each contact pair
# # Which means the outputs were counted multiple times, and were about 2.2 times of history outputs
# # Not in use anymore, please see previous function findcp


# # Reading history output------------------------------------------------------------

# # Ignore this part--------------------Checking the orders of nodeset available according to contact sets
# def Look4History():
#     print step.historyRegions['NodeSet  Z000001'].historyOutputs.keys()
#     print step.historyRegions['NodeSet  Z000002'].historyOutputs.keys()
#     print step.historyRegions['NodeSet  Z000003'].historyOutputs.keys()
#     print step.historyRegions['NodeSet  Z000004'].historyOutputs.keys()
#     print step.historyRegions['NodeSet  Z000005'].historyOutputs.keys()
#     print step.historyRegions['NodeSet  Z000006'].historyOutputs.keys()
#     print step.historyRegions['NodeSet  Z000007'].historyOutputs.keys()
#     print step.historyRegions['NodeSet  Z000008'].historyOutputs.keys()
#     print step.historyRegions['NodeSet  Z000009'].historyOutputs.keys()
#     print step.historyRegions['NodeSet  Z000010'].historyOutputs.keys()
#     print
# #Look4History()
# # Ignore this part--------------------Checking the orders of nodeset available according to contact sets


# # The aim is to find out the contact area on the medial and lateral tibial compartments
# # Look for contact area at medial tibial cartilage due to contact with medial meniscus Z000004
# CA_MED_MEN = "NodeSet  Z000004"
# CAMM = "CAREA    ASSEMBLY_SF_MEDIAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_MED_SELF_CONTACT"
# CAMMvalues = step.historyRegions[CA_MED_MEN].historyOutputs[CAMM].data
# #CFMM = "CFNM     ASSEMBLY_SF_MEDIAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_MED_SELF_CONTACT"
# #CFMMvalues = step.historyRegions[CA_MED_MEN].historyOutputs[CFMM].data

# # Look for contact area at medial tibial cartilage due to contact with femoral cartilage Z000005
# CA_MED_TIB = "NodeSet  Z000005"
# CAMT = "CAREA    ASSEMBLY_SF_TCART_MED_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
# CAMTvalues = step.historyRegions[CA_MED_TIB].historyOutputs[CAMT].data
# #CFMT = "CFNM     ASSEMBLY_SF_TCART_MED_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
# #CFMTvalues = step.historyRegions[CA_MED_TIB].historyOutputs[CFMT].data

# # Look for contact area at lateral tibial cartilage due to contact with lateral meniscus Z000003
# CA_LAT_MEN = "NodeSet  Z000003"
# CALM = "CAREA    ASSEMBLY_SF_LATERAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_LAT_SELF_CONTACT"
# CALMvalues = step.historyRegions[CA_LAT_MEN].historyOutputs[CALM].data
# #CFLM = "CFNM     ASSEMBLY_SF_LATERAL_MEN_SELF_CONTACT/ASSEMBLY_SF_TCART_LAT_SELF_CONTACT"
# #CFLMvalues = step.historyRegions[CA_LAT_MEN].historyOutputs[CFLM].data

# # Look for contact area at lateral tibial cartilage due to contact with femoral cartilage Z000006
# CA_LAT_TIB = "NodeSet  Z000006"
# CALT = "CAREA    ASSEMBLY_SF_TCART_LAT_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
# CALTvalues = step.historyRegions[CA_LAT_TIB].historyOutputs[CALT].data
# #CFLT = "CFNM     ASSEMBLY_SF_TCART_LAT_SELF_CONTACT/ASSEMBLY_SF_FCART_SELF_CONTACT"
# #CFLTvalues = step.historyRegions[CA_LAT_TIB].historyOutputs[CFLT].data

# # This function collects the history contact force and area, and calculates the mean contact pressure
# def Hctps():
#     TCAM = CAMMvalues[-1][1] + CAMTvalues[-1][1]
#     TCAL = CALMvalues[-1][1] + CALTvalues[-1][1]
#     #CFM = CFMMvalues[-1][1]+CFMTvalues[-1][1]
#     #CFL = CFLMvalues[-1][1]+CFLTvalues[-1][1]
#     print 'Medial loading: unknown over ' + str(TCAM)
#     print 'Lateral loading: unknown over ' + str(TCAL)
#     #CTM = CFM/TCAM
#     #CTL = CFL/TCAL
#     #print 'Total history contact pressure at medial: ' + str(CTM)
#     #print 'Total history contact pressure at medial: ' + str(CTL)
#     print
# #Hctps()
# # The history contact force was not requested in shared (Rob's) model setup file
# # To keep the setup.py consistent as this stage, this function was not called
# # Not in use anymore, please see previous function findcp


# myOdb.close()
