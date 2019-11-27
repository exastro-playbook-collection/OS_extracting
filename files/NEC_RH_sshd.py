import os
import json
import re
import sys


args = sys.argv
key_table=[]
if (len(args) < 2):
  sys.exit(1)

path = args[1]

result = {}
# result['VAR_NEC_RH_sshd_config'] = None
# result['become_user'] = 'yes'

config_path = path + '/file/etc/ssh/sshd_config'
if os.path.isfile(config_path):
    config_result = open(config_path)
    str_line = config_result.readline()
    option_result = {}
    while str_line != '':
        ssh_dict={}
        str_match = re.match('(#+)', str_line.strip())
        if str_match == None:
            str_line=str_line.strip()
            str_array = ' '.join(str_line.replace('\n','').replace('\t',' ').split(' ',1)).split(' ',1)
            for index in range(len(str_array)):
                str_array[index]=str_array[index].strip()
            if len(str_array) >= 2:
                ssh_dict['key'] = str_array[0]
                ssh_dict['value'] = str_array[1]
                key_table.append(ssh_dict)
            str_line = config_result.readline()
        else:
            str_line = config_result.readline()
    config_result.close()
for res in key_table:
    result.setdefault('VAR_NEC_RH_sshd_config',[]).append(res)

print (json.dumps(result))
