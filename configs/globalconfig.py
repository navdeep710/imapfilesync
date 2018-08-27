#intention of this module is to be singleton and well available to all
import configparser
import os
import json

config = {}
rawconfig = {}

def poplulateconfig(configfilelocation):
    pass

def getconfig(keyname):
    global config
    if keyname in config:
        return config[keyname]
    else:
        raise ValueError

def getlistforkey(key):
    return json.loads(key)


def parseconfig(filelocation="configs/config.ini"):
    global config, rawconfig
    parser = configparser.ConfigParser()
    parser.read(filelocation)
    rawconfig = parser
    for section in parser.sections():
        for key in parser[section]:
            config[key] = parser[section][key]
    return rawconfig

def getrawconfig():
    global rawconfig
    return rawconfig