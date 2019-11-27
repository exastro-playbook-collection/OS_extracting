import re
import json
import sys
import os
args = sys.argv

if (len(args) < 2):
    sys.exit(1)

path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename1 = path + "/command/1/stdout.txt"
filename2 = path + "/command/0/stdout.txt"
filename3 = path + "/command/3/stdout.txt"

result={}
test_dict_new={}
if os.path.isfile(filename2):
    with open(filename2) as file_object:
        line = file_object.read()
        w_d_name = line.strip()

if os.path.isfile(filename1):
    with open(filename1) as file_object:
        line = file_object.read()
        machine_state = line.strip()
if machine_state == 'True' :
    if os.path.isfile(filename3):
        with open(filename3) as file_object:
            lines = file_object.readlines()
            for index in range(len(lines)):
                if w_d_name in lines[index]:
                    addr = lines[index+1].split(':')[1].strip()
            # test_result = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", line_all)
    test_dict_new['name']=w_d_name
    test_dict_new['ip']=addr
    test_dict_new['user']='input new domin user name'
    test_dict_new['password']='input new domian user password'
    result['VAR_NEC_WIN_hostname_domain']=test_dict_new
    result['VAR_NEC_WIN_hostname_type']= 'domain'
else :
    result['VAR_NEC_WIN_hostname_workgroup']=w_d_name
    result['VAR_NEC_WIN_hostname_type']= 'workgroup'

result['VAR_NEC_WIN_hostname_reboot']= False
print(json.dumps(result))


