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
filename2 = path + "/command/1/stdout.txt"
rootList = []
for root in os.walk(path + '/file'):
    rootList.append(root)
filename_tmp = rootList[-1][0] + '/bootstat.dat'

result_dict = {}
recoverTime = {}
recoveros_DebugInfo = {}
recoveros_DebugInfo['alwaysKeepMemoryDump'] = False
if os.path.isfile(filename):
    fo = open(filename)
    alllines = fo.readlines()
    defaultOS_displayname = None
    guid = None
    pattern_tmp = None
    for strLine in alllines:
        str_match = re.match('default\s*(.*)', strLine)
        if str_match is not None:
            guid = str_match.group(1)
            break
    for strLine in alllines:
        pattern = 'identifier\s*' + guid + '.*'
        str_match = re.match(pattern, strLine)
        if str_match is not None:
            pattern_tmp = 'description\s*(.*)'
            continue
        if pattern_tmp is not None:
            str_match_tmp = re.match(pattern_tmp, strLine)
            if str_match_tmp is not None:
                defaultOS_displayname = str_match_tmp.group(1).strip()
                break
    if defaultOS_displayname is not None:
        result_dict['VAR_WIN_recoveros_defaultOS_displayname'] = defaultOS_displayname
    fo.close()

if os.path.isfile(filename_tmp):
    filename1_1 = path + "/file/hex.txt"
    com_str = 'hexdump -C ' + filename_tmp + ' >> ' + filename1_1
    os.system(com_str)
    fo = open(filename1_1)
    alllines = fo.readlines()
    lines_list = (' '.join(alllines[0].split())).split()
    if int(lines_list[9], 16) == 1:
        recoverTime['enabled'] = True
    if int(lines_list[9], 16) == 0:
        recoverTime['enabled'] = False
    recoverTime['timeout'] = int(lines_list[10], 16)
    if len(recoverTime) > 0:
        result_dict['VAR_WIN_recoveros_recoverTime'] = recoverTime
    fo.close()
    os.remove(filename1_1)

if os.path.isfile(filename2):
    fo = open(filename2)
    alllines = fo.readlines()
    str_filterPages = None
    str_CrashDumpEnabled = None
    for str_line in alllines:
        str_filterPages_match = re.match('\s*FilterPages\s*REG_DWORD\s*(.*)', str_line)
        if str_filterPages_match is not None:
            str_filterPages = int((str_filterPages_match.group(1)).strip(), 16)
        str_CrashDumpEnabled_match = re.match('\s*CrashDumpEnabled\s*REG_DWORD\s*(.*)', str_line)
        if str_CrashDumpEnabled_match is not None:
            str_CrashDumpEnabled = int((str_CrashDumpEnabled_match.group(1)).strip(), 16)
        if str_CrashDumpEnabled is not None:
            if str_CrashDumpEnabled == 0:
                recoveros_DebugInfo['crashDumpEnabled'] = 'none'
            elif str_CrashDumpEnabled == 1:
                if str_filterPages is not None:
                    if str_filterPages == 1:
                        recoveros_DebugInfo['crashDumpEnabled'] = 'active'
                    else:
                        recoveros_DebugInfo['crashDumpEnabled'] = 'perfect'
                else:
                    recoveros_DebugInfo['crashDumpEnabled'] = 'perfect'
            elif str_CrashDumpEnabled == 2:
                recoveros_DebugInfo['crashDumpEnabled'] = 'kernel'
            elif str_CrashDumpEnabled == 3:
                recoveros_DebugInfo['crashDumpEnabled'] = 'min'
            elif str_CrashDumpEnabled == 7:
                recoveros_DebugInfo['crashDumpEnabled'] = 'auto'
        str_dump_match = re.match('\s*DumpFile\s*REG_EXPAND_SZ\s*(.*)', str_line)
        if str_dump_match is not None:
            recoveros_DebugInfo['dump'] = (str_dump_match.group(1)).strip()
        str_overwrite_match = re.match('\s*Overwrite\s*REG_DWORD\s*(.*)', str_line)
        if str_overwrite_match is not None:
            if int((str_overwrite_match.group(1)).strip(), 16) == 1:
                recoveros_DebugInfo['overWrite'] = True
            else:
                recoveros_DebugInfo['overWrite'] = False
        str_alwaysKeepMemoryDump_match = re.match('\s*AlwaysKeepMemoryDump\s*REG_DWORD\s*(.*)', str_line)
        if str_alwaysKeepMemoryDump_match is not None:
            if int((str_alwaysKeepMemoryDump_match.group(1)).strip(), 16) == 1:
                recoveros_DebugInfo['alwaysKeepMemoryDump'] = True
            else:
                recoveros_DebugInfo['alwaysKeepMemoryDump'] = False
    if len(recoveros_DebugInfo) > 0:
        result_dict['VAR_WIN_recoveros_DebugInfo'] = recoveros_DebugInfo
    fo.close()

print (json.dumps(result_dict))