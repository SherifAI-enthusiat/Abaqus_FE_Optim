from itertools import product
import sys
sys.path.append("/nobackup/mnsaz/Mengoni_tool/Test")
import numpy as np
import ParamTools as par

# Coordinate generation
problem = {
    'num_vars': 9,
    'names': ['E1', 'E2', 'E3', 'v12','v13', 'v23', 'G12','G13', 'G23'],
    'bounds': [[0.01, 20],
               [0.01, 20],
               [1, 100],
               [0.01, 0.08],
               [0.01, 0.8],
               [0.01, 0.8],
               [1, 10],
               [1, 30],
               [1, 30]]}
# Generating the number of division in bounds
# ndiv = 16 # This is the number of divisions I want to have
newndiv = [10,10,30,5,5,5,6,15,15] 

# Filter using transverse Isotropic and Material stability 
def filter(X):
    if par.transverseIso(X) ==1:
    ## I will use this to check for material stability
        if par.material_stability(X) == 1:
            str2write = "%s \n"%list(X)
            with open(filename,"a") as file:
                file.writelines(str2write)
    return
# Param generator and 
filename = "/nobackup/mnsaz/Mengoni_tool/param_values.ascii"
# filename1 = "/nobackup/mnsaz/Mengoni_tool/counter.txt"
iterm = par.ParamGenerator(problem,newndiv)

#
for ind,X in enumerate(par.iter_tools(*iterm)):
	filter(X)
