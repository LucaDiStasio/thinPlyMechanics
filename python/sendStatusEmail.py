#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016 Université de Lorraine & Luleå tekniska universitet
Author: Luca Di Stasio <luca.distasio@gmail.com>
                       <luca.distasio@ingpec.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

=====================================================================================

DESCRIPTION

Automatic initialization of Working Directory.

Tested with Python 2.7 Anaconda 2.4.1 (64-bit) distribution
       Matlab R2007b, R2012a
       Windows 7 Integral Edition, Windows 10.

'''

import sys
import os
from os.path import isfile, join
import re
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP       # secure SMTP protocol (port 465, uses SSL)
# from smtplib import SMTP                 # standard SMTP protocol   (port 25, no encryption)

def getUser(folder,file,server):
    with open(join(folder,file),'r') as txt:
        lines = txt.readlines()
    for line in lines:
        if server in line.split()[0]:
            return line.split()[1].replace(' ','').replace('\n','').replace(',','')
            
def getPwd(folder,file,server):
    with open(join(folder,file),'r') as txt:
        lines = txt.readlines()
    for line in lines:
        if server in line.split()[0]:
            return line.split()[2].replace(' ','').replace('\n','').replace(',','')

def sendStatusEmail(folder,file,server,sender,destination,subject,message):
    text_subtype = 'plain'
    try:
        msg = MIMEText(message,text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = destination
        
        conn = SMTP(server)
        conn.set_debuglevel(False)
        conn.login(getUser(folder,file,server), getPwd(folder,file,server))
        try:
            conn.sendmail(sender,destination,msg.as_string())
        finally:
            conn.quit()
    except Exception, e:
        print('Failed to send email:')
        print(e)
        sys.exc_clear()

def main(argv):
    print('Automatic Email Sender')

if __name__ == "__main__":
    main(sys.argv[1:])
    