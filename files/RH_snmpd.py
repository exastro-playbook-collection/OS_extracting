import re
import json
import sys
import os

args = sys.argv

if (len(args) < 2):
    sys.exit(1)

key_table = {}


path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]
filename = path + '/file/etc/snmp/snmpd.conf'
filename1 = path + '/file/etc/snmp/snmptrapd.conf'
result = {}
com2sec_list = []
group_list = []
view_list = []
access_list = []
community_list=[]
user_list=[]
notificationEvent_list=[]
monitor_list=[]
trap_manager_list=[]
trap_agent_dict={}
syslocation=''
syscontact=''
if os.path.isfile(filename):
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            elif (re.match('\s*com2sec\s*(.*)', line) != None):
                line = line.strip('\n')
                text =' '.join(line.split()).split(' ')
                test = {}
                if len(text)==4:
                    test['sec_name'] = text[1]
                    test['source'] = text[2]
                    test['community'] = text[3]
                elif '-Cn' in line:
                    test['sec_name'] = text[3]
                    test['source'] = text[4]
                    test['community'] = text[5]
                if not test in com2sec_list:
                    com2sec_list.append(test)
            elif (re.match('\s*group\s*(.*)', line) != None):
                line = line.strip('\n')
                text =' '.join(line.split()).split(' ')
                test = {}
                if len(text)==4:
                    test['groupName'] = text[1]
                    test['securityModel'] = text[2]
                    test['securityName'] = text[3]
                if not test in group_list:
                    group_list.append(test)
            elif (re.match('\s*view\s*(.*)', line) != None):
                line = line.strip('\n')
                text =' '.join(line.split()).split(' ')
                test = {}
                if len(text)==4:
                    test['name'] = text[1]
                    test['incl_excl'] = text[2]
                    test['subtree'] = text[3]
                elif len(text)==5:
                    test['name'] = text[1]
                    test['incl_excl'] = text[2]
                    test['subtree'] = text[3]
                    test['mask'] = text[4]
                if not test in view_list:
                    view_list.append(test)
            elif (re.match('\s*access\s*(.*)', line) != None):
                line = line.strip('\n')
                text =' '.join(line.split()).split(' ')
                test = {}
                if len(text)==9:
                    test['group'] = text[1]
                    test['context'] = text[2]
                    test['sec_model'] = text[3]
                    test['sec_level'] = text[4]
                    test['prefix'] = text[5]
                    test['read'] = text[6]
                    test['write'] = text[7]
                    test['notif'] = text[8]
                if not test in access_list:
                    access_list.append(test)
            elif (re.match('\s*syslocation\s*(.*)', line) != None):
                line = line.strip('\n')
                line = line.replace('syslocation ','')
                line = line.strip()
                syslocation = line
            elif (re.match('\s*syscontact\s*(.*)', line) != None):
                line = line.strip('\n')
                line = line.replace('syscontact ','')
                line = line.strip()
                syscontact = line
            elif (re.match('\s*trap2sink\s*(.*)', line) != None):
                tra_man_dict={}
                text = []
                line = line.strip('\n')
                text =' '.join(line.split()).split(' ')
                tra_man_dict['trapcommunity'] = text[2]
                tra_man_dict['manager_ip'] = text[1]
                if not tra_man_dict in community_list:
                    community_list.append(tra_man_dict)
            elif (re.match('\s*createUser\s*(.*)', line) != None):
                user_dict={}
                text = []
                ine = line.strip('\n')
                text =' '.join(line.split()).split(' ')
                user_dict['username'] = text[1]
                user_dict['hashmode'] = text[2]
                user_dict['password'] = text[3].replace('"','')
                if not user_dict in user_list:
                    user_list.append(user_dict)
            elif (re.match('\s*notificationEvent\s*(.*)', line) != None):
                notifica_dict = {}
                text = []
                text = ' '.join(line.split()).split(' ')
                ENAME = text[1]
                if '-m' in line or '-o' in line or '-i' in line:
                    OPTIONS = '-' + line.split('-',1)[1].strip('\n')
                    line = line.replace('notificationEvent','')
                    line = line.replace(ENAME,'')
                    line = line.replace(OPTIONS,'')
                    NOTIFICATION = line.strip()
                else:
                    line = line.replace('notificationEvent','')
                    line = line.replace(ENAME,'')
                    NOTIFICATION = line.strip()
                    OPTIONS = ''
                if not ENAME == '':
                    notifica_dict['ENAME'] = ENAME
                if not OPTIONS == '':
                    notifica_dict['OPTIONS'] = OPTIONS
                if not NOTIFICATION == '':
                    notifica_dict['NOTIFICATION'] = NOTIFICATION
                if not notifica_dict in notificationEvent_list:
                    notificationEvent_list.append(notifica_dict)
            elif (re.match('\s*monitor\s*(.*)', line) != None):
                text = []
                monitor_dict = {}
                TX = re.match('.*-e\s+([^\\s]*).*',line)
                ENAME = TX.group(1)
                text = line.split('"')
                EXPRESSION = text[-1]
                NAME = text[1]
                line = line.replace('monitor','')
                line = line.replace('-e','')
                line = line.replace(ENAME,'')
                line = line.replace(NAME,'')
                line = line.replace(EXPRESSION,'')
                line = line.replace('"','').strip()
                OPTIONS = line
                if not ENAME =='':
                    monitor_dict['ENAME'] = ENAME.strip()
                if not OPTIONS =='':
                    monitor_dict['OPTIONS'] = OPTIONS.strip()
                if not EXPRESSION =='':
                    monitor_dict['EXPRESSION'] = EXPRESSION.strip()
                if not NAME =='':
                    monitor_dict['NAME'] = NAME
                if not monitor_dict in monitor_list:
                    monitor_list.append(monitor_dict)

if os.path.isfile(filename1):
    with open(filename1) as file_object:
        lines = file_object.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            elif (re.match('\s*authCommunity\s*(.*)', line) != None):
                line = line.strip('\n')
                text =' '.join(line.split()).split(' ')
                test = {}
                test['behavior'] = text[1]
                test['trapcommunity'] = text[2]
                if not test in trap_manager_list:
                    trap_manager_list.append(test)

if not community_list ==[]:
    trap_agent_dict['community']=community_list
if not user_list ==[]:
    trap_agent_dict['user']=user_list
if not notificationEvent_list ==[]:
    trap_agent_dict['notificationEvent']=notificationEvent_list
if not monitor_list ==[]:
    trap_agent_dict['monitor']=monitor_list


if not com2sec_list ==[]:
    key_table['com2sec'] = com2sec_list
if not group_list ==[]:
    key_table['group'] = group_list
if not view_list ==[]:
    key_table['view'] = view_list
if not access_list ==[]:
    key_table['access'] = access_list
if not syslocation =='':
    key_table['syslocation'] = syslocation
if not syscontact =='':
    key_table['syscontact'] = syscontact
if not trap_agent_dict =={}:
    key_table['trap_agent'] = trap_agent_dict
if not trap_manager_list ==[]:
    key_table['trap_manager'] = trap_manager_list


if not key_table=={}:
    result['VAR_RH_snmpd_info'] = key_table
print(json.dumps(result))
