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

filename0 = path + '/command/0/stdout.txt'
filename1 = path + '/command/1/stdout.txt'
filename2 = path + '/command/2/stdout.txt'
filename3 = path + '/command/3/stdout.txt'
filename4 = path + '/command/4/stdout.txt'
result_dict = {}

nicStatus_List = []
if os.path.isfile(filename0):
    fo = open(filename0)
    alllines = fo.readlines()
    nicStatus_dict = {}
    nic_name = None
    status = None
    for str_line in alllines:
        nic_match = re.match('\s*Name\s*:(.*)', str_line)
        if nic_match is not None:
            nic_name = nic_match.group(1).strip()
            nicStatus_dict['nic_name'] = nic_match.group(1).strip()
        if nic_name is not None:
            status_match = re.match('\s*Status\s*:(.*)', str_line)
            if status_match is not None:
                nicStatus_dict['status'] = status_match.group(1).strip().lower()
                status = status_match.group(1).strip()
                nic_name = None
        if status is not None:
            guid_match = re.match('\s*InstanceID\s*:\s*{(.*)}', str_line)
            if guid_match is not None:
                nicStatus_dict['guid'] = guid_match.group(1).strip()
                nicStatus_List.append(nicStatus_dict)
                status = None
                nicStatus_dict = {}
    fo.close()

nicIP_list = []
if os.path.isfile(filename1):
    fo = open(filename1)
    alllines = fo.readlines()
    nic_name1 = None
    ipaddress = None
    nicIP_dict = {}
    for str_line in alllines:
        nic_match1 = re.match('\s*InterfaceAlias\s*:(.*)', str_line)
        if nic_match1 is not None:
            nic_name1 = nic_match1.group(1).strip()
            nicIP_dict['nic_name'] = nic_match1.group(1).strip()
        if nic_name1 is not None:
            ipadress_match = re.match('\s*IPAddress\s*:(.*)', str_line)
            if ipadress_match is not None:
                nicIP_dict['ipadress'] = ipadress_match.group(1).strip()
                ipaddress = ipadress_match.group(1).strip()
                nic_name1 = None
        if ipaddress is not None:
            perfixLength_match = re.match('\s*PrefixLength\s*:(.*)', str_line)
            if perfixLength_match is not None:
                nicIP_dict['prefixLength'] = perfixLength_match.group(1).strip()
                nicIP_list.append(nicIP_dict)
                ipaddress = None
                nicIP_dict = {}
    fo.close()

nicGateway_list = []
if os.path.isfile(filename2):
    fo = open(filename2)
    alllines = fo.readlines()
    nic_name2 = None
    nicGateway_dict = {}
    for str_line in alllines:
        nic_match2 = re.match('\s*InterfaceAlias\s*:(.*)', str_line)
        if nic_match2 is not None:
            nic_name2 = nic_match2.group(1).strip()
            nicGateway_dict['nic_name'] = nic_match2.group(1).strip()
        if nic_name2 is not None:
            gateway_match = re.match('\s*IPv4DefaultGateway\s*:(.*)', str_line)
            if gateway_match is not None:
                nicGateway_dict['gateway'] = gateway_match.group(1).strip()
                nicGateway_list.append(nicGateway_dict)
                nic_name2 = None
                nicGateway_dict = {}
    fo.close()

dhcp_list = []
if os.path.isfile(filename3):
    fo = open(filename3)
    alllines = fo.readlines()
    nic_name3 = None
    dhcp_dict = {}
    for str_line in alllines:
        nic_match3 = re.match('\s*InterfaceAlias\s*:(.*)', str_line)
        if nic_match3 is not None:
            nic_name3 = nic_match3.group(1).strip()
            dhcp_dict['nic_name'] = nic_match3.group(1).strip()
        if nic_name3 is not None:
            dhcp_match = re.match('\s*Dhcp\s*:(.*)', str_line)
            if dhcp_match is not None:
                if dhcp_match.group(1).strip() == 'Enabled':
                    dhcp_dict['dhcp'] = True
                else:
                    dhcp_dict['dhcp'] = False
                dhcp_list.append(dhcp_dict)
                nic_name3 = None
                dhcp_dict = {}
    fo.close()

netbios_list = []
if os.path.isfile(filename4):
    fo = open(filename4)
    alllines = fo.readlines()
    interfaceID = None
    netbios_dict = {}
    for str_line in alllines:
        interfaceID_match = re.match('HKEY_LOCAL_MACHINE.*Tcpip_{(.*)}', str_line)
        if interfaceID_match is not None:
            interfaceID = interfaceID_match.group(1).strip()
            netbios_dict['guid'] = interfaceID_match.group(1).strip()
        if interfaceID is not None:
            netbios_match = re.match('\s*NetbiosOptions\s*REG_DWORD\s*(.*)', str_line)
            if netbios_match is not None:
                netbios_state = int(netbios_match.group(1).strip(), 16)
                if netbios_state == 0:
                    netbios_dict['netbios'] = 'dhcp'
                elif netbios_state == 1:
                    netbios_dict['netbios'] = 'enabled'
                else:
                    netbios_dict['netbios'] = 'disabled'
                netbios_list.append(netbios_dict)
                interfaceID = None
                netbios_dict = {}
    fo.close()


networkInterface_list = []
networkInterface_dict = {}
networkInterfaceIP_list = []
ipaddresses_dict = {}
networkInterfaceIP_dict = {}
for nicStatus in nicStatus_List:
    networkInterface_dict['name'] = nicStatus['nic_name']
    networkInterface_dict['state'] = nicStatus['status']
    for netbios in netbios_list:
        if nicStatus['guid'].upper() == netbios['guid'].upper():
            networkInterface_dict['netbios'] = netbios['netbios']
            break
    for dhcp in dhcp_list:
        if nicStatus['nic_name'] == dhcp['nic_name']:
            networkInterface_dict['dhcp'] = dhcp['dhcp']
            break
    for nicIP in nicIP_list:
        for nicGateway in nicGateway_list:
            if (nicIP['nic_name'] == nicStatus['nic_name']) and (nicIP['nic_name'] == nicGateway['nic_name']):
                ipaddresses_dict['ip'] = nicIP['ipadress']
                ipaddresses_dict['prefix'] = nicIP['prefixLength']
                ipaddresses_dict['gateway'] = nicGateway['gateway']
                networkInterfaceIP_list.append(ipaddresses_dict)
                networkInterface_dict['ipaddresses'] = networkInterfaceIP_list
                ipaddresses_dict = {}
                networkInterfaceIP_dict = {}
                networkInterfaceIP_list = []
                break
    networkInterface_list.append(networkInterface_dict)
    networkInterface_dict = {}

result_dict['VAR_WIN_network_interface'] = networkInterface_list
print (json.dumps(result_dict))