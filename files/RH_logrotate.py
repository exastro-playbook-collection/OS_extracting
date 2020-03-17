import os
import json
import sys

args = sys.argv

if (len(args) < 2):
    sys.exit(1)

path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename = path + "/file/etc/logrotate.d"

dict_list = {'VAR_RH_logrotate_d_files': None}
if os.path.isdir(filename):
  file_list = os.listdir(filename)
  dict_list = {'VAR_RH_logrotate_d_files': file_list}

print (json.dumps(dict_list))