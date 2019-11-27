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
team_file = path + '/command/0/stdout.txt'
team_interface_file = path + '/command/1/stdout.txt'
team_members_file = path + '/command/2/stdout.txt'
result = {}
team_name = []
team_info_dict= {}
teaming_list = []


if not os.path.isfile(team_file):
    sys.exit(1)
if not os.path.isfile(team_interface_file):
    sys.exit(1)
if not os.path.isfile(team_members_file):
    sys.exit(1)


with open(team_file) as file_object:
    lines =file_object.readlines()

# Get information about each teaming
for line in lines:
    str_match = re.match('Name\s*:\s*(.*)', line)
    if str_match is not None:
        team_info_dict['name'] = str_match.group(1).strip()
    str_match = re.match('TeamingMode\s*:\s*(.*)', line)
    if str_match is not None:
        team_info_dict['mode'] = str_match.group(1).strip()
    str_match = re.match('LoadBalancingAlgorithm\s*:\s*(.*)', line)
    if str_match is not None:
        team_info_dict['lb_argorithm'] = str_match.group(1).strip()

    str_match = re.match('Status\s*:\s*(.*)', line)
    if str_match is not None:
        team_name.append(team_info_dict)
        team_info_dict = {}

# Get network card information and interface information for each teaming
for item in team_name:
    interface_list = []
    members_list = []
    teaming_dict = {}
    with open(team_interface_file) as file_object:
        lines =file_object.readlines()
    for index in range(len(lines)):
        interface_dict = {}
        if lines[index].startswith('Team'):
            if lines[index].split(':')[1].strip() == item['name']:
                if lines[index+3].split(':')[1].strip() == 'False':
                    interface_dict['name'] = lines[index-2].split(':')[1].strip()
                    interface_dict['vlan_id'] = int(lines[index+1].split(':')[1].strip())
                    interface_list.append(interface_dict)
    with open(team_members_file) as file_object:
        lines =file_object.readlines()
    for index in range(len(lines)):
        members_dict = {}
        if lines[index].startswith('Team'):
            if lines[index].split(':')[1].strip() == item['name']:
                members_dict['name'] = lines[index-2].split(':')[1].strip()
                members_dict['mode'] = lines[index+1].split(':')[1].strip()
                members_list.append(members_dict)
    teaming_dict['name'] = item['name']
    teaming_dict['mode'] = item['mode']
    teaming_dict['lb_argorithm'] = item['lb_argorithm']
    if interface_list != []:
        teaming_dict['interfaces'] = interface_list
    teaming_dict['members'] = members_list
    teaming_list.append(teaming_dict)
if teaming_list != []:
    result['VAR_NEC_WIN_teaming'] = teaming_list

print(json.dumps(result))
