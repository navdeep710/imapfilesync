#this module is responsible for fetching imap files
#this is supposed to be a idempotent , meaning its my way or no way
class IMapFetcher():
    def __init__(self,imapcredentials,locallocation):
        self.credentials = imapcredentials
        self.location = locallocation

    #make connection and return
    def connect(self):
        pass


    #list unread emails
    def getunreademails(self):
        pass

    #download attachments, can this be parrallelised
    def downloadattachmentforemail(self,emailid):
        pass
