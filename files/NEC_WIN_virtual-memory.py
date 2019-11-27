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
filename = path + "/command/0/stdout.txt"
size_dict={}
memory_dict={}
result={}
if os.path.isfile(filename):
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            if line.startswith('PagingFiles'):
                memory_macth = re.match('PagingFiles\s*:\s*{(.*)}', line)
                system_macth=re.match('(.*)\s+[0]\s+[0]', memory_macth.group(1))
                if memory_macth.group(1) != None:
                    if memory_macth.group(1) == '':
                        memory_dict['type'] = 'none'
                    elif memory_macth.group(1) == '?:\pagefile.sys':
                        memory_dict['type'] = 'auto'
                    elif system_macth != None:
                        system = system_macth.group(1).replace(':\pagefile.sys','')
                        memory_dict['drive'] = system
                        memory_dict['type'] = 'system'
                    else:
                        text = memory_macth.group(1).replace(':\pagefile.sys','')
                        text =' '.join(text.split()).split(' ')
                        memory_dict['type'] = 'custom'
                        memory_dict['drive'] = text[0]
                        size_dict['min'] = int(text[1])
                        size_dict['max'] = int(text[2])
                        memory_dict['size'] = size_dict
if memory_dict != {}:
    result['VAR_NEC_WIN_virtual_memory'] = memory_dict
result['VAR_NEC_WIN_virtual_memory_reboot']=False
print(json.dumps(result))

