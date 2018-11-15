#encoding:utf-8

import sys,os
import commands
from config import base_path

def check_server():
    ls_command = 'ls -l ' + base_path
    status,output = commands.getstatusoutput(ls_command)
    return output[1]