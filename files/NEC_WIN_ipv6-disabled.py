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
filename = path + "/command/0/stdout.txt"
filename1 = path + "/command/1/stdout.txt"
filename2 = path + "/command/2/stdout.txt"

result_dict = {}
result_dict['VAR_NEC_WIN_ipv6Disabled_reboot'] = False
if os.path.isfile(filename):
    fo = open(filename)
    alllines = fo.readlines()
    ipv6Disabled_tunnel_tmp = ''
    for strLine in alllines:
        if 'DisabledComponents' in strLine:
            ipv6Disabled_tunnel = {'tunnelIpTls': False, 'tunnelCp': False, 'preferIpv4': False, 'native': False,
                                   'tunnelTeredo': False, 'tunnelIsatap': False, 'tunnel6to4': False, 'tunnel': False}
            strList = (' '.join(strLine.split())).split()
            if len(strList) == 3:
                ipv6Disabled_tunnel_tmp = strList[2]
                bin_str = bin(int(ipv6Disabled_tunnel_tmp, 16))
                strList = list(bin_str)
                strList.reverse()
                list_tmp = ['0', '0', '0', '0', '0', '0', '0', '0']
                find_index = strList.index('b')
                i = 0
                while i < len(strList):
                    if i == find_index:
                        break
                    list_tmp[i] = strList[i]
                    i = i + 1
                if list_tmp[0] == '1':
                    ipv6Disabled_tunnel['tunnel'] = True
                if list_tmp[1] == '1':
                    ipv6Disabled_tunnel['tunnel6to4'] = True
                if list_tmp[2] == '1':
                    ipv6Disabled_tunnel['tunnelIsatap'] = True
                if list_tmp[3] == '1':
                    ipv6Disabled_tunnel['tunnelTeredo'] = True
                if list_tmp[4] == '1':
                    ipv6Disabled_tunnel['native'] = True
                if list_tmp[5] == '1':
                    ipv6Disabled_tunnel['preferIpv4'] = True
                if list_tmp[6] == '1':
                    ipv6Disabled_tunnel['tunnelCp'] = True
                if list_tmp[7] == '1':
                    ipv6Disabled_tunnel['tunnelIpTls'] = True
            result_dict['VAR_NEC_WIN_ipv6Disabled_tunnel'] = ipv6Disabled_tunnel
    fo.close()

nicList = []
if os.path.isfile(filename1):
    fo = open(filename1)
    alllines = fo.readlines()
    for strLine in alllines:
        if 'Name' in strLine:
            str_tmp = strLine.split(':')
            if len(str_tmp) == 2:
                nicList.append(str_tmp[1].strip())
    fo.close()

if len(nicList) > 0:
    if os.path.isfile(filename2):
        nicInfoList = []
        fo = open(filename2)
        alllines = fo.readlines()
        for strLine in alllines:
            for nicName in nicList:
                pattern_str = nicName + '\s*' + 'ms_tcpip6' + '\s*' + '(.*)'
                match_str = re.match(pattern_str, strLine.strip())
                if match_str is not None:
                    nicDict = {}
                    nicDict['nicName'] = nicName
                    if match_str.group(1) == 'True':
                        nicDict['state'] = 'enabled'
                    else:
                        nicDict['state'] = 'disabled'
                    nicInfoList.append(nicDict)
        result_dict['VAR_NEC_WIN_ipv6Disabled_NICs'] = nicInfoList
        fo.close()

print (json.dumps(result_dict))
