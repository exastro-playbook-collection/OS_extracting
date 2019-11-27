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
filename = path + '/file/C:/Windows/System32/drivers/etc/hosts'
filename0 = path + '/command/0/stdout.txt'
filename1 = path + '/command/1/stdout.txt'
filename2 = path + '/command/2/stdout.txt'
result_dict = {}

if os.path.isfile(filename):
    fo = open(filename)
    alllines = fo.readlines()
    resolve_host_list = []
    for str_line in alllines:
        if re.match('^\s*#+.*', str_line) is not None:
            continue
        resolve_host = {}
        str_match = re.match('^\s*(\S+)\s*([^#]*).*', str_line)
        if str_match is not None:
            resolve_host['ip'] = str_match.group(1).strip()
            resolve_host['hostname'] = str_match.group(2).strip()
        if len(resolve_host) > 0:
            resolve_host_list.append(resolve_host)
    if len(resolve_host_list) > 0:
        result_dict['VAR_NEC_WIN_name_resolve_hosts'] = resolve_host_list

nicList = []
if os.path.isfile(filename0):
    fo = open(filename0)
    alllines = fo.readlines()
    for str_line in alllines:
        nic_match = re.match('\s*Name\s*:(.*)', str_line)
        if nic_match is not None:
            nicList.append(nic_match.group(1).strip())
    fo.close()

serverAddrDict_list = []
if os.path.isfile(filename1):
    fo = open(filename1)
    alllines = fo.readlines()
    nic_name = None
    interface_addr = {}
    for str_lines in alllines:
        for nic in nicList:
            pattern = 'InterfaceAlias\s*:\s*' + nic + '\W*'
            interface_match = re.match(pattern, str_lines)
            if interface_match is not None:
                nic_name = nic
                interface_addr['interface'] = nic
                break
            if nic_name is not None:
                serverAddr_match = re.match('ServerAddresses\s*:\s*{(.*)}', str_lines)
                if serverAddr_match is not None:
                    interface_addr['addrList'] = serverAddr_match.group(1).strip().replace(' ', '').split(',')
                    serverAddrDict_list.append(interface_addr)
                    nic_name = None
                    interface_addr = {}
    fo.close()

suffixDict_list = []
if os.path.isfile(filename2):
    fo = open(filename2)
    alllines = fo.readlines()
    nic_name = None
    inter_suffix = {}
    for str_lines in alllines:
        for nic in nicList:
            pattern = 'InterfaceAlias\s*:\s*' + nic + '\W*'
            interface_match = re.match(pattern, str_lines)
            if interface_match is not None:
                nic_name = nic
                inter_suffix['interface'] = nic
                continue
            if nic_name is not None:
                serverAddr_match = re.match('ConnectionSpecificSuffix\s*:\s*(.*)', str_lines)
                if serverAddr_match is not None:
                    inter_suffix['suffix'] = serverAddr_match.group(1).strip()
                    suffixDict_list.append(inter_suffix)
                    nic_name = None
                    inter_suffix = {}
    fo.close()

dnsList = []
for suffix in suffixDict_list:
    dns_dict = {}
    for serverAddr in serverAddrDict_list:
        if suffix['interface'] == serverAddr['interface']:
            dns_dict['nic_name'] = serverAddr['interface']
            dns_dict['servers'] = serverAddr['addrList']
            dns_dict['suffix'] = suffix['suffix']
            dnsList.append(dns_dict)

if len(dnsList) > 0:
    result_dict['VAR_NEC_WIN_name_resolve_dns'] = dnsList
print (json.dumps(result_dict))