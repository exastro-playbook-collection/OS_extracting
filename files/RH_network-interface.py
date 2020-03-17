import re
import json
import sys
import os

args = sys.argv

if (len(args) < 2):
    sys.exit(1)

key_table = []
interface_list = []
ipaddr_list = []
path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename = path + "/file/etc/sysconfig/network-scripts"
result = {}
if (not os.path.isdir(filename)):
    print(json.dumps(result))
    sys.exit(0)

for root, dirs, files in os.walk(filename):
    for file_interface in files:
        if 'ifcfg-' in file_interface and file_interface != 'ifcfg-lo' and ':' not in file_interface:
            interface_list.append(file_interface)
if len(interface_list) == 0:
    print(json.dumps(result))
    sys.exit(0)

for inter_file in interface_list:
    dict_inter1 = {}
    dict_inter2 = {}
    face_name = inter_file.split('-',1)[1]
    dict_inter1['name'] = face_name
    if (not os.path.isfile(filename+'/'+inter_file)):
        print(json.dumps(result))
        sys.exit(0)
    file_object = open(filename+'/'+inter_file)
    lines = file_object.readlines()
    for line in lines:
        line = line.strip('\n')
        if line.startswith('IPADDR'):
            interface_ip = line.split('=')[1]
            dict_inter2['ip'] = interface_ip
        elif line.startswith('GATEWAY'):
            interface_gate = line.split('=')[1]
            dict_inter2['gateway'] = interface_gate
        elif line.startswith('PREFIX'):
            interface_prefix = line.split('=')[1]
            dict_inter2['prefix'] = interface_prefix
        elif line.startswith('NETMASK'):
            exchange_mask = lambda mask: sum(bin(int(i)).count('1') for i in mask.split('.'))
            interface_prefix = exchange_mask(line.split('=')[1])
            dict_inter2['prefix'] = interface_prefix
        elif line.startswith('BOOTPROTO'):
            if 'dhcp' in line:
                interface_dhcp = True
            else:
                interface_dhcp = False
            dict_inter1['dhcp'] = interface_dhcp
        elif line.startswith('ONBOOT'):
            interface_state = line.split('=')[1]
            dict_inter1['state'] = interface_state
    ipaddr_list.append(dict_inter2)
    dict_inter1['ipaddresses'] = ipaddr_list
    ipaddr_list = []
    key_table.append(dict_inter1)
    file_object.close()

for res in key_table:
    result.setdefault("VAR_RH_network_interface",[]).append(res)

print(json.dumps(result))
