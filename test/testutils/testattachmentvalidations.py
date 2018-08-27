from configs import globalconfig
from utils import attachmentvalidations
import os
import unittest

def getcurrentdir():
    return os.path.abspath(os.path.dirname(__file__))


class testfilevalidations(unittest.TestCase):
    def testextension(self):
        rawconfig = globalconfig.parseconfig(getcurrentdir() + "/filenameconfig.ini")
        print(getcurrentdir())
        self.assertEqual(attachmentvalidations.validatefilename("watsup.xlsx", rawconfig), True)


    def testunavailableextension(self):
        rawconfig = globalconfig.parseconfig(getcurrentdir() + "/filenameconfig.ini")
        print(getcurrentdir())
        self.assertEqual(attachmentvalidations.validatefilename("watsup.xlsx2", rawconfig), False)


    def testnonefile(self):
        rawconfig = globalconfig.parseconfig(getcurrentdir() + "/filenameconfig.ini")
        print(getcurrentdir())
        self.assertEqual(attachmentvalidations.validatefilename(None, rawconfig), False)
