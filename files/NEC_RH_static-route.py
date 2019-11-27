import re
import json
import sys
import os

args = sys.argv

if (len(args) < 2):
    sys.exit(1)

key_table = []
interface_name = []
file_list = []
interface_list = []

path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename1 = path + "/file/etc/sysconfig/network-scripts"
filename2 = path + "/file/etc/sysconfig/network"
result = {}
if os.path.isdir(filename1):
    for root, dirs, files in os.walk(filename1):
        for file_interface in files:
            if file_interface.startswith('route-'):
                interface_list.append(file_interface)
    for inter_file in interface_list:
        face = inter_file.split('-',1)[1]
        file_object = open(filename1+'/'+inter_file)
        lines = file_object.readlines()
        for line in lines:
            line = line.strip('\n')
            if 'metric' in line:
                text =' '.join(line.split()).split(' ')
                de = text[0]
                ga = text[2]
                me = text[4]
                static_route1 = {}
                static_route1['interface'] = face
                static_route1['dest'] = de
                static_route1['gateway'] = ga
                static_route1['metric'] = me
                key_table.append(static_route1)
            else:
                line = line.strip('\n')
                text =' '.join(line.split()).split(' ')
                de = text[0]
                ga = text[2]
                static_route2 = {}
                static_route2['interface'] = face
                static_route2['dest'] = de
                static_route2['gateway'] = ga
                key_table.append(static_route2)
            file_object.close()

if os.path.isfile(filename2):
    with open(filename2) as file_object:
        lines = file_object.readlines()
        GATEWAY = {}
        for line in lines:
            if not line.startswith('GATEWAY='): 
                continue
            else:
                line = line.strip('\n')
                line = line.split('=')[1]
                line = line.strip()
                GATEWAY['gateway'] = line
                key_table.append(GATEWAY)


for res in key_table:
    result.setdefault("VAR_NEC_static_route",[]).append(res)

print(json.dumps(result))
