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
filename = path + "/command/1/stdout.txt"
filename1 = path + "/command/2/stdout.txt"
filename2 = path + "/command/3/stdout.txt"
ntp_server=[]
ntp_data_time_dict={}
result={}
ntp_dict={}
# Generate a file for VAR_WIN_ntp_DataTime
if os.path.isfile(filename):
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            server_macth = re.match('\d+\s*:\s*(.*)', line)
            if line.startswith('(default)'):
                default_macth = re.match('\(default\)\s*:\s*(\d+)', line)
                ntp_data_time_dict['default'] = int(default_macth.group(1))
            elif server_macth != None:
                ntp_server.append(server_macth.group(1).strip())
if ntp_server != []:
    ntp_data_time_dict['Servers'] = ntp_server

# Generate a file for VAR_WIN_ntp
if os.path.isfile(filename1):
    with open(filename1) as file_object:
        lines = file_object.readlines()
        for line in lines:
            ntp_server_macth = re.match('NtpServer\s*:\s*(.*)', line)
            if ntp_server_macth != None:
                ntp_dict['NtpServer'] = ntp_server_macth.group(1).strip()
            type_macth = re.match('Type\s*:\s*(.*)', line)
            if type_macth != None:
                ntp_dict['Type'] = type_macth.group(1).strip()

if os.path.isfile(filename2):
    with open(filename2) as file_object:
        lines = file_object.readlines()
        for line in lines:
            cross_macth = re.match('CrossSiteSyncFlags\s*:\s*(.*)', line)
            if cross_macth != None:
                ntp_dict['CrossSiteSyncFlags'] = int(cross_macth.group(1).strip())
            resolve_max_macth = re.match('ResolvePeerBackoffMaxTimes\s*:\s*(.*)', line)
            if resolve_max_macth != None:
                ntp_dict['ResolvePeerBackoffMaxTimes'] = int(resolve_max_macth.group(1).strip())
            resolve_min_macth = re.match('ResolvePeerBackoffMinutes\s*:\s*(.*)', line)
            if resolve_min_macth != None:
                ntp_dict['ResolvePeerBackoffMinutes'] = int(resolve_min_macth.group(1).strip())
            special_macth = re.match('SpecialPollInterval\s*:\s*(.*)', line)
            if special_macth != None:
                ntp_dict['SpecialPollInterval'] = int(special_macth.group(1).strip())
            event_macth = re.match('EventLogFlags\s*:\s*(.*)', line)
            if event_macth != None:
                ntp_dict['EventLogFlags'] = int(event_macth.group(1).strip())

if ntp_dict != {}:
    result['VAR_WIN_ntp'] = ntp_dict
result['VAR_WIN_ntp_DataTime'] = ntp_data_time_dict
print(json.dumps(result))

