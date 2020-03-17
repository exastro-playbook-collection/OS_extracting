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
filename3 = path + "/command/3/stdout.txt"
net_frame_features = ''
net_frame_core = ''
net_http_activation = ''
net_non_http_activ = ''
result_dict = {}
result_dict['VAR_WIN_dotNET35_reboot'] = False
if os.path.isfile(filename):
    fo = open(filename)
    alllines = fo.readlines()
    for line in alllines:
        if 'NET-Framework-Features' in line:
            strList = (' '.join(line.split())).split()
            if len(strList) > 3:
                net_frame_features = strList[-1]
    fo.close()

if os.path.isfile(filename1):
    fo = open(filename1)
    alllines = fo.readlines()
    for line in alllines:
        if 'NET-Framework-Core' in line:
            strList = (' '.join(line.split())).split()
            if len(strList) > 3:
                net_frame_core = strList[-1]
    fo.close()

if os.path.isfile(filename2):
    fo = open(filename2)
    alllines = fo.readlines()
    for line in alllines:
        if 'NET-HTTP-Activation' in line:
            strList = (' '.join(line.split())).split()
            if len(strList) > 3:
                net_http_activation = strList[-1]
    fo.close()

if os.path.isfile(filename3):
    fo = open(filename3)
    alllines = fo.readlines()
    for line in alllines:
        if 'NET-Non-HTTP-Activ' in line:
            strList = (' '.join(line.split())).split()
            if len(strList) > 3:
                net_non_http_activ = strList[-1]
    fo.close()

nameList = ''
if net_frame_features == 'Installed' :
    nameList = 'NET-Framework-Features'
if net_frame_core == 'Installed' :
    if nameList.strip() == '': 
        nameList = nameList + 'NET-Framework-Core,'
    else:
        nameList = nameList + ',NET-Framework-Core'
if net_http_activation == 'Installed' :
    if nameList.strip() == '': 
        nameList = nameList + 'NET-HTTP-Activation,'
    else:
        nameList = nameList + ',NET-HTTP-Activation'
if net_non_http_activ == 'Installed' :
    if nameList.strip() == '': 
        nameList = nameList + 'NET-Non-HTTP-Activ'
    else:
        nameList = nameList + ',NET-Non-HTTP-Activ'
result_dict['VAR_dotNET35_Feature_Name'] = nameList
result_dict['VAR_dotNET35_Installer_Name'] = 'microsoft-windows-netfx3-ondemand-package.cab'

print (json.dumps(result_dict))