#! /usr/bin/env python3
# pw.py - An insecure password locker program.
PASSWORDS={'email':'pkorts01','blog':'nonose','luggage':'12345'}

import sys, pyperclip
if len(sys.argv) <2:
    print('Usage: python pw.py [account] - copy account password')
    sys.exit()

account= sys.argv[1]  # first command line arg is the account name


if account in PASSWORDS:
    pyperclip.copy(PASSWORDS[account])
    print('Password for ' + account + ' copied to clipboard.')
else:
    print ('there is no account named '+account)
    
