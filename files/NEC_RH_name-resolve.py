import re
import json
import sys
import os

args = sys.argv

if (len(args) < 2):
    sys.exit(1)

key_table1 = []
key_table2 = []
key_table3 = []
path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename = path + "/file/etc/hosts"
filename1 = path + "/file/etc/resolv.conf"
filename2 = path + "/file/etc/nsswitch.conf"
result = {}
if os.path.isfile(filename):
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            if 'localhost' in line or line.startswith('#'):
                continue
            else:
                host = {}
                line = line.strip('\n')
                text =' '.join(line.split()).split(' ')
                if len(text) >=2:
                    ip = text[0]
                    hostname = text[1]
                    host['ip'] = ip
                    host['hostname'] = hostname
                    key_table1.append(host)

if os.path.isfile(filename1):
    with open(filename1) as file_object:
        lines = file_object.readlines()
        name_server_list=[]
        suff_list=[]
        for line in lines:
            if line.startswith('search'):
                line = line.strip('\n')
                suff_list =' '.join(line.split()).split(' ')
                suff_list.remove('search')
            if line.startswith('nameserver'):
                line = line.strip('\n')
                name_server =' '.join(line.split()).split(' ')
                if len(name_server) >= 2:
                    name_server_list.append(name_server[1])
    if name_server_list ==[] and suff_list !=[]:
        result['VAR_NEC_RH_name_resolve_dns']={'suffix':suff_list}
    if name_server_list !=[] and suff_list ==[]:
        result['VAR_NEC_RH_name_resolve_dns']={'servers':name_server_list}
    if name_server_list !=[] and suff_list !=[]:
        result['VAR_NEC_RH_name_resolve_dns']={'servers':name_server_list,'suffix':suff_list }
if os.path.isfile(filename2):
    with open(filename2) as file_object:
        lines = file_object.readlines()
        nsswitch_list=[]
        nsswitch_tmp_list=[]
        for line in lines:
            if line.startswith('hosts:'):
                line = line.strip('\n')
                nsswitch_tmp_list= ' '.join(line.split()).split(' ')
                nsswitch_tmp_list.remove('hosts:')
    for index in range(len(nsswitch_tmp_list)):
        nsswitch_dict={}
        if '[' in nsswitch_tmp_list[index] and ']'in nsswitch_tmp_list[index]:
            continue
        elif not (index+2)>len(nsswitch_tmp_list):
            if '[' in nsswitch_tmp_list[index+1] and ']'in nsswitch_tmp_list[index+1]:
                nsswitch_dict['method']=nsswitch_tmp_list[index]
                nsswitch_dict['actions']=nsswitch_tmp_list[index+1]
            else:
                nsswitch_dict['method']=nsswitch_tmp_list[index]
        else:
            nsswitch_dict['method']=nsswitch_tmp_list[index]
        key_table3.append(nsswitch_dict)

for res in key_table1:
    result.setdefault('VAR_NEC_RH_name_resolve_hosts',[]).append(res)

result.setdefault('VAR_NEC_RH_name_resolve_ipv6_disabled',False)
for res in key_table3:
    result.setdefault('VAR_NEC_RH_name_resolve_nsswitch',[]).append(res)
print(json.dumps(result))


