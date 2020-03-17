import os
import json
import sys
import re

args = sys.argv
if (len(args) < 2):
    sys.exit(1)
path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename = path + "/command/0/stdout.txt"
filename1 = path + "/command/1/stdout.txt"
filename2 = path + "/command/2/stdout.txt"
#ConsentPromptBehaviorAdmin
cpba_int = 0
#PromptOnSecureDesktop
posd_int = 0
#EnableLUA
elua_int = 0
result_dict = {}
result_dict['VAR_WIN_uac_reboot'] = False
if os.path.isfile(filename):
    fo = open(filename)
    alllines = fo.readlines()
    for strLine in alllines:
        if 'ConsentPromptBehaviorAdmin' in strLine:
            strList = (' '.join(strLine.split())).split()
            if len(strList) == 3:
                uac_tmp = strList[2]
                cpba_int = int(uac_tmp, 16)
    fo.close()

if os.path.isfile(filename1):
    fo = open(filename1)
    alllines = fo.readlines()
    for strLine in alllines:
        if 'PromptOnSecureDesktop' in strLine:
            strList = (' '.join(strLine.split())).split()
            if len(strList) == 3:
                uac_tmp = strList[2]
                posd_int = int(uac_tmp, 16)	
    fo.close()
if os.path.isfile(filename2):
    fo = open(filename2)
    alllines = fo.readlines()
    for strLine in alllines:
        if 'EnableLUA' in strLine:
            strList = (' '.join(strLine.split())).split()
            if len(strList) == 3:
                uac_tmp = strList[2]
                elua_int = int(uac_tmp, 16)
    fo.close()

if cpba_int ==  1 and posd_int == 1 and elua_int == 1:
    result_dict['VAR_WIN_uac'] = 'high1'

if cpba_int ==  2 and posd_int == 1 and elua_int == 1:
    result_dict['VAR_WIN_uac'] = 'high2'

if cpba_int ==  3 and posd_int == 0 and elua_int == 1:
    result_dict['VAR_WIN_uac'] = 'high3'

if cpba_int ==  4 and posd_int == 0 and elua_int == 1:
    result_dict['VAR_WIN_uac'] = 'high4'

if cpba_int ==  5 and posd_int == 1 and elua_int == 1:
    result_dict['VAR_WIN_uac'] = 'middle'

if cpba_int ==  5 and posd_int == 0 and elua_int == 1:
    result_dict['VAR_WIN_uac'] = 'low'

if cpba_int ==  0 and posd_int == 0 and elua_int == 0:
    result_dict['VAR_WIN_uac'] = 'disabled'

if cpba_int ==  0 and posd_int == 0 and elua_int == 1:
    result_dict['VAR_WIN_uac'] = 'disabled'

print (json.dumps(result_dict))