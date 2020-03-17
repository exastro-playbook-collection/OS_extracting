import os
import json
import sys
import re

args = sys.argv
if (len(args) < 2):
    sys.exit(1)
path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename1 = path + "/command/1/stdout.txt"
filename3 = path + "/command/3/stdout.txt"
SeTcbPrivilegeList = []
SeIncreaseQuotaPrivilegeList = []
SeChangeNotifyPrivilegeList  = []
SeImpersonatePrivilegeList = []
SeServiceLogonRightList = []
SeDenyServiceLogonRightList = []
SeSecurityPrivilegeList = []
SeAssignPrimaryTokenPrivilegeList = []

result_dict = {}
if os.path.isfile(filename1):
    fo = open(filename1)
    alllines = fo.readlines()
    for strLine in alllines:
        if 'SeTcbPrivilege' in strLine:
            SeTcbPrivilegeList = ('='.join(strLine.split('=')[1:])).replace('*', '').strip().split(',')
        if 'SeIncreaseQuotaPrivilege' in strLine:
            SeIncreaseQuotaPrivilegeList = ('='.join(strLine.split('=')[1:])).replace('*', '').strip().split(',')
        if 'SeChangeNotifyPrivilege' in strLine:
            SeChangeNotifyPrivilegeList = ('='.join(strLine.split('=')[1:])).replace('*', '').strip().split(',')
        if 'SeImpersonatePrivilege' in strLine:
            SeImpersonatePrivilegeList = ('='.join(strLine.split('=')[1:])).replace('*', '').strip().split(',')
        if 'SeServiceLogonRight' in strLine:
            SeServiceLogonRightList = ('='.join(strLine.split('=')[1:])).replace('*', '').strip().split(',')
        if 'SeDenyServiceLogonRight' in strLine:
            SeDenyServiceLogonRightList = ('='.join(strLine.split('=')[1:])).replace('*', '').strip().split(',')
        if 'SeSecurityPrivilege' in strLine:
            SeSecurityPrivilegeList = ('='.join(strLine.split('=')[1:])).replace('*', '').strip().split(',')
        if 'SeAssignPrimaryTokenPrivilege' in strLine:
            SeAssignPrimaryTokenPrivilegeList = ('='.join(strLine.split('=')[1:])).replace('*', '').strip().split(',')
    fo.close()

userRightsAssign_list = []
userRightsAssign_dict = {}
SeTcbPrivilege_user_list = []
SeIncreaseQuotaPrivilege_user_list = []
SeChangeNotifyPrivilege_user_list = []
SeImpersonatePrivilege_user_list = []
SeServiceLogonRight_user_list = []
SeDenyServiceLogonRight_user_list = []
SeSecurityPrivilege_user_list = []
SeAssignPrimaryTokenPrivilege_user_list = []

if os.path.isfile(filename3):
    fo = open(filename3)
    alllines = fo.readlines()
    for strLine in alllines:
        userSID = strLine.strip().split(" ")[-1]
        userName = strLine.replace(userSID, '').strip()
        if len(SeTcbPrivilegeList) > 0:
            for str in SeTcbPrivilegeList:
                if str == userName or str == userSID:
                    SeTcbPrivilege_user_list.append(userName)
        if len(SeIncreaseQuotaPrivilegeList) > 0:
            for str in SeIncreaseQuotaPrivilegeList:
                if str == userName or str == userSID:
                    SeIncreaseQuotaPrivilege_user_list.append(userName)
        if len(SeChangeNotifyPrivilegeList) > 0:
            for str in SeChangeNotifyPrivilegeList:
                if str == userName or str == userSID:
                    SeChangeNotifyPrivilege_user_list.append(userName)
        if len(SeImpersonatePrivilegeList) > 0:
            for str in SeImpersonatePrivilegeList:
                if str == userName or str == userSID:
                    SeImpersonatePrivilege_user_list.append(userName)
        if len(SeServiceLogonRightList) > 0:
            for str in SeServiceLogonRightList:
                if str == userName or str == userSID:
                    SeServiceLogonRight_user_list.append(userName)
        if len(SeDenyServiceLogonRightList) > 0:
            for str in SeDenyServiceLogonRightList:
                if str == userName or str == userSID:
                    SeDenyServiceLogonRight_user_list.append(userName)
        if len(SeSecurityPrivilegeList) > 0:
            for str in SeSecurityPrivilegeList:
                if str == userName or str == userSID:
                    SeSecurityPrivilege_user_list.append(userName)
        if len(SeAssignPrimaryTokenPrivilegeList) > 0:
            for str in SeAssignPrimaryTokenPrivilegeList:
                if str == userName or str == userSID:
                    SeAssignPrimaryTokenPrivilege_user_list.append(userName)
    if len(SeTcbPrivilege_user_list) > 0:
        userRightsAssign_dict['name'] = 'SeTcbPrivilege'
        userRightsAssign_dict['user'] = SeTcbPrivilege_user_list
        userRightsAssign_dict['action'] = 'add'    
        userRightsAssign_list.append(userRightsAssign_dict)
        userRightsAssign_dict = {}

    if len(SeIncreaseQuotaPrivilege_user_list) > 0:
        userRightsAssign_dict['name'] = 'SeIncreaseQuotaPrivilege'
        userRightsAssign_dict['user'] = SeIncreaseQuotaPrivilege_user_list
        userRightsAssign_dict['action'] = 'add'    
        userRightsAssign_list.append(userRightsAssign_dict)
        userRightsAssign_dict = {}
    
    if len(SeChangeNotifyPrivilege_user_list) > 0:
        userRightsAssign_dict['name'] = 'SeChangeNotifyPrivilege'
        userRightsAssign_dict['user'] = SeChangeNotifyPrivilege_user_list
        userRightsAssign_dict['action'] = 'add'
        userRightsAssign_list.append(userRightsAssign_dict)
        userRightsAssign_dict = {}
    
    if len(SeImpersonatePrivilege_user_list) > 0:
        userRightsAssign_dict['name'] = 'SeImpersonatePrivilege'
        userRightsAssign_dict['user'] = SeImpersonatePrivilege_user_list
        userRightsAssign_dict['action'] = 'add'
        userRightsAssign_list.append(userRightsAssign_dict)
        userRightsAssign_dict = {}
    
    if len(SeServiceLogonRight_user_list) > 0:
        userRightsAssign_dict['name'] = 'SeServiceLogonRight'
        userRightsAssign_dict['user'] = SeServiceLogonRight_user_list
        userRightsAssign_dict['action'] = 'add'
        userRightsAssign_list.append(userRightsAssign_dict)
        userRightsAssign_dict = {}
    
    if len(SeDenyServiceLogonRight_user_list) > 0:
        userRightsAssign_dict['name'] = 'SeDenyServiceLogonRight'
        userRightsAssign_dict['user'] = SeDenyServiceLogonRight_user_list
        userRightsAssign_dict['action'] = 'add'
        userRightsAssign_list.append(userRightsAssign_dict)
        userRightsAssign_dict = {}
    
    if len(SeSecurityPrivilege_user_list) > 0:
        userRightsAssign_dict['name'] = 'SeSecurityPrivilege'
        userRightsAssign_dict['user'] = SeSecurityPrivilege_user_list
        userRightsAssign_dict['action'] = 'add'
        userRightsAssign_list.append(userRightsAssign_dict)
        userRightsAssign_dict = {}
    
    if len(SeAssignPrimaryTokenPrivilege_user_list) > 0:
        userRightsAssign_dict['name'] = 'SeAssignPrimaryTokenPrivilege'
        userRightsAssign_dict['user'] = SeAssignPrimaryTokenPrivilege_user_list
        userRightsAssign_dict['action'] = 'add'
        userRightsAssign_list.append(userRightsAssign_dict)
        userRightsAssign_dict = {}
 
    fo.close()

result_dict['VAR_userRightsAssign_info'] = userRightsAssign_list

print (json.dumps(result_dict))