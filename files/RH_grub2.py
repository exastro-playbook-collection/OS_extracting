import os
import json
import re
import sys


args = sys.argv

if (len(args) < 2):
  sys.exit(1)

path = args[1]

result = {}
result['VAR_RH_grub2_reboot'] = False

option_path = path + '/file/etc/default/grub'

#option_path = 'D:/qcx/mywork/4Q/test/file/grub'
if os.path.isfile(option_path):
    cmdOption_result = open(option_path)
    str_line = cmdOption_result.readline()
    option_result = {}
    while str_line != '':
        str_match = re.match('(#+)', str_line.strip())
        if str_match == None:
            str_array = str_line.strip().split('=', 1)
            for index in range(len(str_array)):
                str_array[index] = str_array[index].strip()
            if len(str_array) == 2:
                if str_array[0] != '' and str_array[1] != '':
                    option_result[str_array[0]] = str_array[1].replace('\"', '')
            str_line = cmdOption_result.readline()
        else:
            str_line = cmdOption_result.readline()
    cmdOption_result.close()
    if option_result != {}:
        result['VAR_RH_grub2_options'] = option_result
print (json.dumps(result))
