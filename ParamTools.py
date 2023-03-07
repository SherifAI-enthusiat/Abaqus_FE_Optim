import math
import numpy as np
from itertools import product


def PoissonCalc(param):
    # This calc is performed in most of the functions 
    var = np.array(param,dtype=float)
    v21 = (var[3]/var[0])*var[1]
    v31 = (var[4]/var[0])*var[2]
    v32 = (var[5]/var[1])*var[2]
    return v21,v31,v32

def determinantCalc(param):
    # Matrix construction for determinant Not very neccessary!
    v21,v31,v32 = PoissonCalc(param)
    array = np.array([]).reshape(0,6)
    var = np.array(param,dtype=float)
    row_1 = "1/%s,-%s/%s,-%s/%s,0,0,0"%(var[0],v21,var[1],v31,var[2])
    row_2 = "-%s/%s,1/%s,-%s/%s,0,0,0"%(var[3],var[0],var[1],v32,var[2])
    row_3 = "-%s/%s,-%s/%s,1/%s,0,0,0"%(var[4],var[0],var[5],var[1],var[2])
    row_4 = "0,0,0,1/%s,0,0"%var[6]
    row_5 = "0,0,0,0,1/%s,0"%var[7]
    row_6 = "0,0,0,0,0,1/%s"%var[8]
    compiled = [row_1,row_2,row_3,row_4,row_5,row_6]
    for row in compiled:
        temp = row.split(",")
        na = [eval(item) for item in temp]
        nrow = np.mat(na)
        array = np.vstack((array,nrow))
    determ = np.linalg.det(array)
    return determ

# Stability criterion using posiitive definite matrix.
def material_stability(param):
    var = np.array(param,dtype=float)
    v21,v31,v32 = PoissonCalc(param) 
    ## Material stability requirements
    fnew = np.hstack((var[0:3],var[6:]))
    criMod = np.all(fnew > 0) # Checks to see if all E1,E2,E3,G1,G2,G3>0
    # (E1/E2)^0.5 (E1/E3)^0.5 & (E2/E3)^0.5
    cr1 = math.sqrt(var[0]/var[1])> abs(var[3])
    cr2 = math.sqrt(var[0]/var[2])> abs(var[4])
    cr3 = math.sqrt(var[1]/var[2])> abs(var[5])
    # cr4 = math.sqrt(var[1]/var[0])> abs(v21)
    # cr5 = math.sqrt(var[2]/var[0])> abs(v31)
    # cr6 = math.sqrt(var[2]/var[1])> abs(v32)
    cr7 = 1 - var[3]*v21 - var[5]*v32 - var[4]*v31 - 2*var[3]*v32*var[4] >0

    if criMod and cr1 and cr2 and cr3 and cr7:
        return True
    else:
        return False

def transverseIso(param):
    var = np.array(param,dtype=float)
    if var[0]==var[1] and var[7]==var[8]:
        _,v31,v32 = PoissonCalc(param) 
       # cr1 = var[0]==var[1] # Ep =E1=E2
        cr2 = v31==v32 # vtp
        cr3 = var[4]==var[5] # vpt
       # cr4 = var[7]==var[8] # Gt
        if cr2 and cr3:    
            return True
        else:
            return  False
    else:
        return False

def iter_tools(*array):
    for param in product(*array):
        yield param

def ParamGenerator(data,num_div):
    # The purpose of this function is to generate some parameters for us
    nlist = {}
    for ind,item in enumerate(data['bounds']):
        nlist[ind] = np.linspace(item[0],item[1],num_div[ind]) 
    
    # Form a list for itertool.product()
    temp =[] # Dynamic list container
    for ind,_ in enumerate(nlist):
        temp.append(nlist[ind])
    return temp

