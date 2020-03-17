import re
import json
import sys
import os

args = sys.argv

if (len(args) < 2):
    sys.exit(1)

key_table = []
rsyslog = {}
path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename = path + '/file/etc/rsyslog.conf'
filename1 = path + '/file/etc/rsyslog.d'
result = {}
if (not os.path.isfile(filename)):
    print(json.dumps(result))
    sys.exit(0)
with open(filename) as file_object:
    lines = file_object.readlines()
    for line in lines:
        line = line.strip('\n')
        if line.startswith('#') or line.startswith('$') or len(line) ==0 :
            continue
        else:
            line = line.strip('\r')
            rsyslog = {}
            TX = re.match('.*[^\\\\][\s]([^\s]+.*)',line)
            act = TX.group(1)
            # text =' '.join(line.split()).split(' ')
            # le = len(text)
            # act = text[-1]
            line = line.replace(act,'')
            line = line.strip()
            rsyslog['selector'] = line
            rsyslog['action'] = act
            key_table.append(rsyslog)
if (not os.path.isdir(filename1)):
    print(json.dumps(result))
    sys.exit(0)
file_list = os.listdir(filename1)

for res in key_table:
    result.setdefault('VAR_RH_rsyslog_rules',[]).append(res)
for fil in file_list:
    result.setdefault('VAR_RH_rsyslog_d_files',[]).append(fil)
print(json.dumps(result))
