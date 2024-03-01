from itertools import product
import sys,os
sys.path.append("/nobackup/mnsaz/Mengoni_tool/Test")
import numpy as np
import ParamTools as par

# Coordinate generation
problem = {
    'num_vars': 9,
    'names': ['E1', 'E2', 'E3', 'v12','v13', 'v23', 'G12','G13', 'G23'],
    'bounds': [[0.01, 20],
               [0.01, 20],
               [1, 250],
               [0.01],
               [0.01],
               [0.01],
               [1, 20],
               [1, 30],
               [1, 30]]}
# Generating the number of division in bounds
# ndiv = 16 # This is the number of divisions I want to have
newndiv = [5,5,25,1,1,1,6,6,6] 

# Filter using transverse Isotropic and Material stability 
def filter(X,keyword):
    if keyword == "trans" and par.transverseIso(X) == True:
    ## I will use this to check for material stability
        if par.material_stability(X) == True:
            str2write = "%s \n"%list(X)
            with open(filename,"a") as file:
                file.writelines(str2write)
    elif keyword =="ortho" and par.material_stability(X)==True:
        str2write = "%s \n"%list(X)
        with open(filename,"a") as file:
            file.writelines(str2write)
    return
# Param generator and 
filename = os.path.join(os.getcwd(),"param_values.csv")
# filename1 = "/nobackup/mnsaz/Mengoni_tool/counter.txt"
iterm = par.ParamGenerator(problem,newndiv)

#
for ind,X in enumerate(par.iter_tools(*iterm)):
	filter(X,"trans")
