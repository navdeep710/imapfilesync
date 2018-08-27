import argparse
import importlib
import os
import threading
import time
import json

from configs import globalconfig
from copier.CopyToNodes import copytonodes
from testutils import emailutils
from configs.globalconfig import getrawconfig
from testutils.fileconvertor import csv_from_excel

storagemodule = importlib.import_module("reliablestorage.localstorage")

def parse_argument():
    parser = argparse.ArgumentParser(description='Process ImapFileSync parameters')
    parser.add_argument('--config',help="pass configuration file path",required=True)
    parser.add_argument('--service',help="if you want to run as a service you can pass start as value ")
    parser.add_argument('--watermarkstorage',help="two options , local or email",default="local",choices=["local","email"])
    args = parser.parse_args()
    return args


def runfrompreviouswatermark():
    #fetch previous watermark
    watermark = storagemodule.getvalue()
    print("running from previous watermark {0}".format(watermark))
    #fetch emails from watermark
    result,data = emailutils.fetchemailsfrompreviouswatermark(watermark)
    email_ids = data[0].split()
    if(emailutils.checkifwatermarkisgreaterthanlastid(watermark, email_ids[-1])):
        print("no new emails found since the old watermark")
        return
    for email in email_ids:
        #download email
        filepath = emailutils.downloadattachment(email, getrawconfig()['download']['location'])
        #there can be some emails which does not have attachments or valid attachments
        if filepath:
            #convert from excel to csv , this can be replaced with more generic convertors
            csvs = csv_from_excel(filepath)
            #copy downloaded file to cluster nodes nodes,localfile,remotebasepath
            copy_successful = [copytonodes(json.loads(getrawconfig()["copy"]["nodes"]),file,getrawconfig()["copy"]["remotepath"]) for file in csvs ]
            #if copy is not successful just log it for now, we can keep the files as its and note delete it
            if(all(copy_successful)):
                os.remove(filepath)
        #i am saving watermark for every file we are putting in, even it got failed
        storagemodule.setvalue(bytes.decode(email))


def runTimerThread(deamon=False):
    thread = threading.Thread(runfrompreviouswatermark)
    thread.daemon = deamon
    print("starting timer thread")
    thread.start()
    return thread


def servicerunner():
    timerthread = runTimerThread()
    while True:
        if(not timerthread.isAlive()):
            timerthread = runTimerThread()
        time.sleep(int(getrawconfig()["scrapetimer"]["buffer"]))


def run():
    # with daemon.basic_daemonize("pid.info"):
    servicerunner()

if __name__ == '__main__':
    args = parse_argument()
    config_file_location = args.config
    globalconfig.parseconfig(config_file_location)
    storagemodule = importlib.import_module("reliablestorage.{0}storage".format(getrawconfig()["watermark"]["storage"]))
    if args.service is None:
        runfrompreviouswatermark()
    else:
        run()


