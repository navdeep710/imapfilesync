import persistqueue
from exceptions import customexceptions

queues = {}

#currently i am creating a uniquue queue with mutl
def createqueue(queuename,queuelocation):
    mqueue = persistqueue.SQLiteAckQueue(queuelocation,multithreading=True)
    queues[queuename] = mqueue

#this method will produce the queue if not present ,so dont be heckless in get method
def getqueue(queuename,queuelocation):
    if(queuename not in queues):
        createqueue(queuename,queuelocation)
    return queues[queuename]

#you can also think of making this as synchronized
#this is assuming that you have created the queue otherwise i will bite you
def getitemfromqueue(queuename):
    if(queuename in queues):
        return getqueue(queuename).get()
    else:
        raise customexceptions.queuenotfound("{0} queue not created yet".format(queuename))

