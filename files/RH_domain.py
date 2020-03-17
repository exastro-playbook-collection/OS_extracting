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
filename = path + '/file/etc/hosts'
domain_name_file = path + '/command/1/stdout.txt'
domain_ip_file = path + '/command/2/stdout.txt'
result = {}
domain_name =''
domain_ip =''
if os.path.isfile(domain_name_file):
    with open(domain_name_file) as file_object:
        line =file_object.read()
        line = line.replace('domain-name:','')
        domain_name = line.strip()

if os.path.isfile(domain_ip_file):
    with open(domain_ip_file) as file_object:
        line =file_object.read()
        line = line.replace('Server:','')
        domain_ip = line.strip()
hostname = ''
if os.path.isfile(filename) and domain_name != '' and domain_ip !='':
    with open(filename) as file_object:
        lines =file_object.readlines()
        for line in lines:
            if line.startswith(domain_ip):
                text =' '.join(line.split()).split(' ')
                if len(text) >=2:
                    if domain_name in text[1]:
                        hostname = text[1]
if domain_name != '' and domain_ip != '' and hostname != '':
    key_table['hostname'] = hostname
    key_table['hostip'] = domain_ip
    key_table['domainname'] = domain_name
    key_table['user'] = 'update by user'
    key_table['password'] = '*****'
    result['VAR_RH_domain'] = key_table
    print(json.dumps(result))
else:
    print(json.dumps(result))


