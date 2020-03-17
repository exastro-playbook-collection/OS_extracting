import os
import json
import sys
import re

args = sys.argv
#agrv[0]=xxx.py;argv[1]=collect_root
if (len(args) < 2):
    sys.exit(1)
path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
result_dict = {}
result_dict['VAR_WIN_dnsSuffix_reboot'] = False
nicList = []
filename0 = path + '/command/0/stdout.txt'
filename5 = path + '/command/5/stdout.txt'
filename6 = path + '/command/6/stdout.txt'

if os.path.isfile(filename0):
    specific_dict = {}
    fo = open(filename0)
    alllines = fo.readlines()
    for strLine in alllines:
        str_match = re.match('\s*UseDomainNameDevolution\s*REG_DWORD\s*(.*)', strLine)
        if str_match is not None:
            useDomainNameDevolution = int((str_match.group(1).strip()), base=16)
            if useDomainNameDevolution == 1:
                specific_dict['useDomainNameDevolution'] = True
            else:
                specific_dict['useDomainNameDevolution'] = False
        strList_match = re.match('\s*SearchList\s*REG_SZ\s*(.*)', strLine)
        if strList_match is not None:
            searchList = strList_match.group(1).strip().split(',')
            specific_dict['searchList'] = searchList
    if len(specific_dict) > 0:
        result_dict['VAR_WIN_dnsSuffix_specific'] = specific_dict
    fo.close()

if os.path.isfile(filename5):
    fo = open(filename5)
    alllines = fo.readlines()
    for strLine in alllines:
        str_match = re.match('\s*Name\s*:\s*(.*)', strLine)
        if str_match is not None:
            nicList.append(str_match.group(1).strip())
    fo.close()

if os.path.isfile(filename6):
    dnsSuffixNic_list = []
    fo = open(filename6)
    alllines = fo.readlines()
    for strLine in alllines:
        for nicname in nicList:
            strSuffix_match = re.match(nicname + '\s*(.*)', strLine)
            if strSuffix_match is not None:
                sufficname = strSuffix_match.group(1).strip()
                if sufficname != '':
                    dnsSuffixNic_dict = {}
                    dnsSuffixNic_dict['nicName'] = nicname
                    dnsSuffixNic_dict['suffixName'] = sufficname
                    dnsSuffixNic_list.append(dnsSuffixNic_dict)
    if len(dnsSuffixNic_list) > 0:
        result_dict['VAR_WIN_dnsSuffix_nic'] = dnsSuffixNic_list
    fo.close()
print (json.dumps(result_dict))