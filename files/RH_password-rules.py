import os
import json
import re
import sys

args = sys.argv

if (len(args) < 2):
  sys.exit(1)

path = args[1]
result = {}
cmd_path0 = path + '/command/0/stdout.txt'
cmd_path1 = path + '/command/1/stdout.txt'

if os.path.isfile(cmd_path0):
    cmd_result = open(cmd_path0)
    str_line = cmd_result.readline()
    pw_quality_arg1 = []
    i = 0
    if str_line != '':
        str_line = str_line.strip('\n').strip()

        str_match = re.match('.*authtok_type=((\".*\")|(\'.*\')|([^\\s]*))[^\\s]*', str_line)
        if str_match != None:
            str_line = str_line.replace(str_match.group(1), '').strip()
        #endif
        str_match = re.match('.*dictpath=((\".*\")|(\'.*\')|([^\\s]*))[^\\s]*', str_line)
        if str_match != None:
            str_line = str_line.replace(str_match.group(1), '').strip()
        #endif
        str_match = re.match('.*badwords=((\".*\")|(\'.*\')|([^\\s]*))[^\\s]*', str_line)
        if str_match != None:
            str_line = str_line.replace(str_match.group(1), '').strip()
        #endif

        #debug, enforce_for_root, local_users_only, use_authtok
        str_match = re.match('.*(debug).*', str_line)
        if str_match != None:
            pw_quality_arg1.append("debug")
        #endif
        str_match = re.match('.*(enforce_for_root).*', str_line)
        if str_match != None:
            pw_quality_arg1.append("enforce_for_root")
        #endif
        str_match = re.match('.*(local_users_only).*', str_line)
        if str_match != None:
            pw_quality_arg1.append("local_users_only")
        #endif
        str_match = re.match('.*(use_authtok).*', str_line)
        if str_match != None:
            pw_quality_arg1.append("use_authtok")
        #endif
    #endif
    cmd_result.close()
    if pw_quality_arg1:
        result['VAR_RH_pw_quality_arg1'] = pw_quality_arg1
    #endif
#endif

if os.path.isfile(cmd_path1):
    cmd_result = open(cmd_path1)
    str_line = cmd_result.readline()
    pw_authentication_arg1 = []
    i = 0
    if str_line != '':
        str_line = str_line.strip('\n').strip()

        #debug, audit, nullok, try_first_pass, use_first_pass, nodelay, use_authtok, not_set_pass, nis, shadow, md5, bigcrypt, sha256, sha512, blowfish, broken_shadow, no_pass_expiry
        str_match = re.match('.*(debug).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("debug")
        #endif
        str_match = re.match('.*(audit).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("audit")
        #endif
        str_match = re.match('.*(nullok).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("nullok")
        #endif
        str_match = re.match('.*(try_first_pass).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("try_first_pass")
        #endif
        str_match = re.match('.*(use_first_pass).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("use_first_pass")
        #endif
        str_match = re.match('.*(nodelay).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("nodelay")
        #endif
        str_match = re.match('.*(use_authtok).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("use_authtok")
        #endif
        str_match = re.match('.*(not_set_pass).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("not_set_pass")
        #endif
        str_match = re.match('.*(nis).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("nis")
        #endif
        str_match = re.match('.*(shadow).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("shadow")
        #endif
        str_match = re.match('.*(md5).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("md5")
        #endif
        str_match = re.match('.*(bigcrypt).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("bigcrypt")
        #endif
        str_match = re.match('.*(sha256).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("sha256")
        #endif
        str_match = re.match('.*(sha512).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("sha512")
        #endif
        str_match = re.match('.*(blowfish).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("blowfish")
        #endif
        str_match = re.match('.*(broken_shadow).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("broken_shadow")
        #endif
        str_match = re.match('.*(no_pass_expiry).*', str_line)
        if str_match != None:
            pw_authentication_arg1.append("no_pass_expiry")
        #endif

    #endif
    cmd_result.close()
    if pw_authentication_arg1:
        result['VAR_RH_pw_authentication_arg1'] = pw_authentication_arg1
    #endif
#endif

print (json.dumps(result))
