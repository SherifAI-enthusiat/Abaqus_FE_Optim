import os
def writeInp(x,orifile,workspacePath,inpName):
    paramToOpti = list()
    for arg in range(len(x)):
        paramToOpti.append(float(x[arg]))

    workspaceInp = os.path.join(workspacePath,inpName)
    with open(orifile,'r') as oldlines:
        lines = oldlines.readlines()

    # Material property change with regards to menisci and attachement site
    data ={}
    data["spring_locs"] = []
    data['menisci_locs'] = []
    test2 = tuple(float("{:.2f}".format(float(item))) for item in paramToOpti)
    temp3 = '%s\n'%float("{:.2f}".format(test2[2]/15)) # Spring stiffness values
    new_param = str(test2[0])
    for ind,item in enumerate(test2):
        if ind!= 0 and ind <=7:
            new_param = new_param + ', %s'%item
    for ind,item in enumerate(lines):
        if item.startswith('*Spring'):
            data['spring_locs'].append(ind+2)
        elif item.startswith('*Material') and item.endswith('name=MENISCAL_MEN\n'):
            data['menisci_locs'].append(ind+2)

    # Writing to new .INP file
    data['combined'] = data['spring_locs']+data['menisci_locs']
    if not os.path.exists(workspacePath):
        os.makedirs(workspacePath)
    with open(workspaceInp,"w") as file2write:
        for ind,item in enumerate(lines):
            if ind in data['combined']:
                if ind in data['menisci_locs']:
                    if ind== max(data['menisci_locs']):
                        file2write.write(new_param +'\n')
                elif ind in data['spring_locs']:
                    file2write.write(temp3)
            elif ind == max(data['menisci_locs'])+1:
                file2write.write(' '+ str(test2[-1]) +',\n')
            else:
                file2write.write(item)
    return workspaceInp