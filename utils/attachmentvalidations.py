def namevalidation(filename,validation):
    if(filename):
        return filename.startswith(validation)
    return False

def extensionvalidation(filename,validation):
    if(filename):
        return filename.endswith(validation)
    else:
        return False

def validatefilename(filename,rawconfig):
    validation_array = []
    if('start' in rawconfig["filevalidation"]):
        validation_array.append(namevalidation(filename,rawconfig["filevalidation"]["start"]))
    if('ext' in rawconfig["filevalidation"]):
        validation_array.append(extensionvalidation(filename,rawconfig["filevalidation"]["ext"]))
    return all(validation_array)
