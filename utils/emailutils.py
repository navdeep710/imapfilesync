import imaplib
import email
from exceptions.customexceptions import Emailnotfound
import os
from configs.globalconfig import getrawconfig
from configs import globalconfig
import smtplib
from email.mime.text import MIMEText
import json
from reliablestorage import localstorage
from utils.attachmentvalidations import validatefilename


#most of the functions expects a email client connected
#returns a email session
def getmailsession(config_section="readmail"):
    mail = imaplib.IMAP4_SSL(getrawconfig()[config_section].get("imap_ssl"))
    mail.login(getrawconfig()[config_section].get("username"), getrawconfig()[config_section].get("password"))
    #selecting by defauilt inbox as the folder
    mail.select(getrawconfig()[config_section].get("mail_folder"))
    return mail


#this is uid based
def fetchmails(mailsessionfunc=getmailsession,query="ALL"):
    mailsession = mailsessionfunc()
    result,data = mailsession.uid('search',None,query)
    mailsession.close()
    return result,data

def fetchtimedurationemails(mailsessionfunc=getmailsession):
    gettimedurationstring = ""
    fetchmails(mailsessionfunc,gettimedurationstring)

#this will return a watermark stored in email or locally
#this has to be greater than 0
def getpreviouswatermark():
    return localstorage.getvalue()

def fetchemailsfrompreviouswatermark(previous_watermark,mailsessionfunc=getmailsession):
    query_for_emails = makequeryforemailsaboveid(previous_watermark)
    result,data = fetchmails(query=query_for_emails)
    return result,data

def downloadattachment(mailid,downloadlocation,mailsessionfunc=getmailsession):
    mailsession = mailsessionfunc()
    typ, messageParts = mailsession.fetch(mailid, '(RFC822)')
    if typ != 'OK':
        raise Emailnotfound
    emailBody = messageParts[0][1]
    raw_email_string = emailBody.decode('utf-8')
    mail = email.message_from_string(raw_email_string)
    filePath = None
    for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if validatefilename(fileName,getrawconfig()):
            filePath = os.path.join(downloadlocation, 'attachments', bytes.decode(mailid) + "_" + fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
    mailsession.close()
    return filePath



#we are setting watermark in body
def sendemail(value,config_section="readmail"):
    smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
    smtp_ssl_port = 465
    username = getrawconfig()[config_section]["username"]
    password = getrawconfig()[config_section]["password"]
    sender = 'ME@EXAMPLE.COM'
    targets = ['HE@EXAMPLE.COM', 'SHE@EXAMPLE.COM']

    msg = MIMEText(json.dumps({"watermark":value}))
    msg['Subject'] = 'Hello'
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()

def makequeryforemailsaboveid(baseemailid,batchsize="*"):
    return "(UID {0}:{1})".format(str(baseemailid),str(batchsize))


def checkifwatermarkisgreaterthanlastid(watermark,lastid):
    return int(watermark) >= int(bytes.decode(lastid))


if __name__ == '__main__':
    globalconfig.parseconfig("../configs/config.ini")
    result, data = fetchemailsfrompreviouswatermark(75)
    mailids = data[0].split()
    for mid in mailids:
        downloadattachment(mid,"/tmp")

