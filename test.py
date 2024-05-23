import HelperFunc as HP
import subprocess,os

test = HP.testPath()
basePath = os.getcwd()
dataRet = os.path.join(basePath,"dataRetrieval.py")
command = 'abaqus python "%s"'%dataRet
storePath = "MatlabOutput\\Knee 5"
commandn = r'%s -- "%s-%s"'%(command,test,storePath)
pCall2 = subprocess.run(commandn, shell= True, capture_output=True, text=True)
print(pCall2)