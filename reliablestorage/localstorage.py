#each reliable storage need to have a get set property
#here we will be storing value in s3 at predefined path
#and constantly updating it

from configs import globalconfig
import os

def getvalue():
    filename = globalconfig.getrawconfig()["watermark"]["location"]
    if not os.path.isfile(filename):
        return globalconfig.getrawconfig()["watermark"]["default"]
    contents = open(filename,'r')
    firstline = str(contents.readlines()[0]).strip(' \t\n\r')
    contents.close()
    return firstline

def setvalue(value):
    filename = globalconfig.getrawconfig()["watermark"]["location"]
    contents = open(filename,'w')
    contents.write(value)
    contents.close()

