#i am hoping these should be collection of functions since i definitely want it to run in parallel

from paramiko import SSHClient,SSHException
from scp import SCPClient
from decorators.decorator import retry


def makeconnection(hostname,userport=22,username="vagrant",key_filename=None):
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(hostname,port=userport,username=username,timeout=30,key_filename=key_filename)
        return ssh
    except Exception:
        print("unable to make connection to {0}".format(hostname))

#do we need to include date to it, we can include date at the time of download
def getremotefilename(localfilepath,dateofdownload=""):
    #remote filename can be same as local filename too
    return "/tmp/"


#i am not woried about nuber of connections here , as i am closing as soon as file is copied
retry(SSHException,tries=3,backoff=2)
def copyfile(remote_hostname,localfilepath,remotefilepath):
    print("copying file {0} to host {1}".format(localfilepath,remote_hostname))
    try:
        ssh = makeconnection(remote_hostname)
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(localfilepath, remotefilepath)
        ssh.close()
    except Exception:
        "copy failed trying again"
        raise SSHException

def checkfileispresent(remote_hostname,remotefilepath):
    try:
        ssh = makeconnection(remote_hostname)
        sftp = ssh.open_sftp()
        sftp.stat(remotefilepath)
        sftp.close()
        ssh.close()
        return True
    except Exception:
        print("this means file {0} was not found or host is not reachable .please check".format(remote_hostname))
        return False



#i want to create a pipeline effect, hence will copy a single file sequentially to all hosts,
#if one of the copies fails , delete previous node copies
def copytonodes(nodes,localfile,remotebasepath):
    try:
        results = [copyfile(node,localfile,remotebasepath) for node in nodes]
    except Exception:
        print("copying has failed")
    #check if file is present or not
    is_presents = [checkfileispresent(node,remotebasepath) for node in nodes]
    copy_successful = all(is_presents)
    print("copy status :: " + str(copy_successful))
    if not copy_successful:
        #this is where delete files if it is present
        print("deleting all previous copies")
        for node,ispresent in zip(nodes,is_presents):
            if ispresent:
                removefile(node,localfile)
    return copy_successful
    #else we are good


def removefile(remote_hostname,remote_filename):
    try:
        print("removing filename {0} from host: {1}".format(remote_filename,remote_hostname))
        ssh = makeconnection(remote_hostname)
        sftp = ssh.open_sftp()
        sftp.remove(remote_filename)
        sftp.close()
        ssh.close()
    except Exception:
        print("was enable to remove the file from host {0} this is serious!!.please check [send pager]".format(remote_hostname))
