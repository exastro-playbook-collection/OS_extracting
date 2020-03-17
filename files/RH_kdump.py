import os
import json
import re
import sys


args = sys.argv

if (len(args) < 2):
  sys.exit(1)

path = args[1]

result = {}
result['VAR_RH_kdump_reboot'] =  False
cmd_path = path + '/command/2/stdout.txt'
str_state = ''

if os.path.isfile(cmd_path):
    cmd_result = open(cmd_path)
    if 'inactive' in cmd_result.read():
        str_state = 'stopped'
    else:
        str_state = 'started'
    cmd_result.close()
result['VAR_RH_kdump'] = {'state': str_state}

option_path = path + '/file/etc/kdump.conf'
if os.path.isfile(option_path):
    cmdOption_result = open(option_path)
    str_line = cmdOption_result.readline()
    option_result = {}
    while str_line != '':
        str_match = re.match('(#+)', str_line.strip())
        if str_match == None:
            str_array = (re.sub('\s+', ' ', str_line.strip())).split(' ', 1)
#            if (len(str_array) == 1) and (str_array[0] != ''):
#                option_result[str_array[0]] = None
            if len(str_array) == 2:
                option_result[str_array[0]] = str_array[1].strip()
            str_line = cmdOption_result.readline()
        else:
            str_line = cmdOption_result.readline()
    cmdOption_result.close()
    if option_result == {}:
        result['VAR_RH_kdump'] = {'state': str_state}
    else:
        result['VAR_RH_kdump'] = {'state': str_state, 'option': option_result}
print (json.dumps(result))
