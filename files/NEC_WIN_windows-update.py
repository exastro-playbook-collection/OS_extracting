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
filename = path + '/command/1/stdout.txt'
filename0 = path + '/command/0/stdout.txt'
result_dict = {}
userWUserver = None

if os.path.isfile(filename):
    update_AU = {}
    fo = open(filename)
    alllines = fo.readlines()
    str_noAutoUpdate = None
    for str_line in alllines:
        auOption_match = re.match('\s*AUOptions\s*REG_DWORD\s*(.*)', str_line)
        if auOption_match is not None:
            update_AU['AUOptions'] = int(auOption_match.group(1).strip(), base=16)
        automatic_match = re.match('\s*AutomaticMaintenanceEnabled\s*REG_DWORD\s*(.*)', str_line)
        if automatic_match is not None:
            str_automatic = int(automatic_match.group(1).strip(), base=16)
            if str_automatic == 1:
                update_AU['automaticMaintenanceEnabled'] = 'enabled'
            else:
                update_AU['automaticMaintenanceEnabled'] = 'disabled'
        scheduledInstallDay_match = re.match('\s*ScheduledInstallDay\s*REG_DWORD\s*(.*)', str_line)
        if scheduledInstallDay_match is not None:
            update_AU['scheduledInstallDay'] = int(scheduledInstallDay_match.group(1).strip(), base=16)
        scheduledInstallTime_match = re.match('\s* ScheduledInstallTime\s*REG_DWORD\s*(.*)', str_line)
        if scheduledInstallTime_match is not None:
            update_AU['scheduledInstallTime'] = int(scheduledInstallTime_match.group(1).strip(), base=16)
        allowMUUpdateService_match = re.match('\s*AllowMUUpdateService\s*REG_DWORD\s*(.*)', str_line)
        if allowMUUpdateService_match is not None:
            allowMUUpdateService = int(allowMUUpdateService_match.group(1).strip(), base=16)
            if allowMUUpdateService == 1:
                update_AU['allowMUUpdateService'] = 'enabled'
            else:
                update_AU['allowMUUpdateService'] = 'disabled'
        noAutoUpdate_match = re.match('\s*NoAutoUpdate\s*REG_DWORD\s*(.*)', str_line)
        if noAutoUpdate_match is not None:
            str_noAutoUpdate = int(noAutoUpdate_match.group(1).strip(), base=16)
            if str_noAutoUpdate == 1:
                update_AU['status'] = 'disabled'
            else:
                update_AU['status'] = 'enabled'
        userWUserver_match = re.match('\s*UseWUServer\s*REG_DWORD\s*(.*)', str_line)
        if userWUserver_match is not None:
            userWUserver = int(userWUserver_match.group(1).strip(), base=16)
    if str_noAutoUpdate is None:
        update_AU['status'] = 'notConfigured'
    if len(update_AU) > 0:
        result_dict['VAR_NEC_WIN_update_AU'] = update_AU
    fo.close()

if os.path.isfile(filename0):
    update_WU = {}
    update_target = {}
    targetGroupEnabled = None
    fo = open(filename0)
    alllines = fo.readlines()
    for str_line in alllines:
        wuServer_match = re.match('\s*WUServer\s*REG_SZ\s*(.*)', str_line)
        if wuServer_match is not None:
            update_WU['WUServer'] = wuServer_match.group(1).strip()
        wuStatusServer_match = re.match('\s*WUStatusServer\s*REG_SZ\s*(.*)', str_line)
        if wuStatusServer_match is not None:
            update_WU['WUStatusServer'] = wuStatusServer_match.group(1).strip()
        targetGroupEnabled_match = re.match('\s*TargetGroupEnabled\s*REG_DWORD\s*(.*)', str_line)
        if targetGroupEnabled_match is not None:
            targetGroupEnabled = int(targetGroupEnabled_match.group(1).strip(), base=16)
        targetGroup_match = re.match('\s*TargetGroup\s*REG_SZ\s*(.*)', str_line)
        if targetGroup_match is not None:
            update_target['targetGroup'] = targetGroup_match.group(1).strip()
    if userWUserver is not None:
        if userWUserver == 1:
            update_WU['status'] = 'enabled'
        else:
            update_WU['status'] = 'disabled'
    else:
        update_WU['status'] = 'notConfigured'
    if targetGroupEnabled is not None:
        if targetGroupEnabled == 1:
            update_target['status'] = 'enabled'
        else:
            update_target['status'] = 'disabled'
    else:
        update_target['status'] = 'notConfigured'
    if len(update_WU) > 0:
        result_dict['VAR_NEC_WIN_update_WU'] = update_WU
    if len(update_target) > 0:
        result_dict['VAR_NEC_WIN_update_targetGroup'] = update_target
    fo.close()

print (json.dumps(result_dict))