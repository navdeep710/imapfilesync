import os

def getfilename(sourcefile):
    return sourcefile.split('/')[-1]

def renamefiles(files, destinationfolder):
    return [os.sep.join([destinationfolder,getfilename(filepath)]) for filepath in files]

def movefiles(files,destinationfolder):
    newfolder = []
    for file in files:
        newname = os.sep.join([destinationfolder,getfilename(file)])
        os.rename(file,newname)
        newfolder.append(newname)
    return newfolder
