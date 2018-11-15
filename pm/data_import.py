#encoding:utf-8
password = "password"
base_path = "/opt/IBM/wlp/usr/server/"

import sys,os
import commands

def find_path():

    ls_command = 'ls -l ' + base_path
    output = commands.getstatusoutput(ls_command)
    return output
