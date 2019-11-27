import re
import json
import sys
import os

args = sys.argv

if (len(args) < 2):
    sys.exit(1)

key_table = []

path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename = path + "/file/etc/ntp.conf"

result = {}
if (not os.path.isfile(filename)):
    print(json.dumps(result))
    sys.exit(0)

with open(filename) as file_object:
    lines = file_object.readlines()
    for line in lines:
        line = line.strip('\n')
        if not line.startswith('server '):
            continue
        else:
            server = {}
            text =' '.join(line.split()).split(' ')
            if len(text) >=3:
                if 'prefer' in text:
                    server['prefer'] = True
                else:
                    server['prefer'] = False
                server['server'] = text[1]
                server['op'] = 'add'
                key_table.append(server)


result.setdefault('VAR_NEC_RH_ntp_clearflag',True)
for res in key_table:
    result.setdefault("VAR_NEC_RH_ntp_servers",[]).append(res)
print(json.dumps(result))

