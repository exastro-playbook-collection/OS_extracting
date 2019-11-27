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

filename = path + '/command/0/stdout.txt'
result_dict = {}

if os.path.isfile(filename):
    fo = open(filename)
    alllines = fo.readlines()
    result_list = []
    str_currentUser = None
    str_localMachine = None
    for str_line in alllines:
        currentUser_match = re.match('Scope\s*: CurrentUser', str_line)
        if currentUser_match is not None:
            str_currentUser = 'CurrentUser'
            continue
        if str_currentUser is not None:
            currentUserPolicy_match = re.match('ExecutionPolicy\s*: (.*)', str_line)
            if currentUserPolicy_match is not None:
                dict_tmp = {}
                dict_tmp['psexecpolicy'] = currentUserPolicy_match.group(1).strip()
                dict_tmp['psscope'] = str_currentUser
                result_list.append(dict_tmp)
                str_currentUser = None
        localMachine_match = re.match('Scope\s*: LocalMachine', str_line)
        if localMachine_match is not None:
            str_localMachine = 'LocalMachine'
            continue
        if str_localMachine is not None:
            localMachine_match = re.match('ExecutionPolicy\s*: (.*)', str_line)
            if localMachine_match is not None:
                dict_tmp = {}
                dict_tmp['psexecpolicy'] = localMachine_match.group(1).strip()
                dict_tmp['psscope'] = str_localMachine
                result_list.append(dict_tmp)
                str_localMachine = None
    if len(result_list) > 0:
        result_dict['VAR_NEC_WIN_executionPolicy'] = result_list
    fo.close()

print (json.dumps(result_dict))