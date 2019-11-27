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

filename0 = path + "/command/0/stdout.txt"
filename1 = path + "/command/1/stdout.txt"

result_dict = {}

nicList = []
if os.path.isfile(filename1):
    fo = open(filename1)
    alllines = fo.readlines()
    nicIndex_dict = {}
    nicName = None
    for str_line in alllines:
        str_match = re.match('\s*Name\s*:(.*)', str_line)
        if str_match is not None:
            nicName = str_match.group(1).strip()
            nicIndex_dict['name'] = nicName
        if nicName is not None:
            index_match = re.match('\s*ifIndex\s*:(.*)', str_line)
            if index_match is not None:
                nicIndex_dict['ifIndex'] = index_match.group(1).strip()
                nicList.append(nicIndex_dict)
                nicName = None
                nicIndex_dict = {}
    fo.close()

route_list = []
if os.path.isfile(filename0):
    fo = open(filename0)
    alllines = fo.readlines()
    route_dict = {}
    for str_line in alllines:
        if ('ifIndex' in str_line) or ('----' in str_line) or ('\r\n' == str_line):
            continue
        route_match = re.match('(\S*)\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)\W*', str_line)
        if (route_match is not None) and (':' not in route_match.group(2).strip()):
            route_dict['ifIndex'] = route_match.group(1).strip()
            route_dict['dest'] = route_match.group(2).strip()
            route_dict['gateway'] = route_match.group(3).strip()
            route_dict['metric'] = int(route_match.group(4).strip())
            route_list.append(route_dict)
            route_dict = {}
    fo.close()

static_route_list = []
static_route_dict = {}
for route in route_list:
    static_route_dict['dest'] = route['dest']
    static_route_dict['gateway'] = route['gateway']
    static_route_dict['metric'] = route['metric']
    for nicItem in nicList:
        if route['ifIndex'] == nicItem['ifIndex']:
            static_route_dict['interface'] = nicItem['name']
            break
    static_route_list.append(static_route_dict)
    static_route_dict = {}

result_dict['VAR_NEC_WIN_static_route'] = static_route_list
print (json.dumps(result_dict))