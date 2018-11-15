#encoding:utf-8

import json
import sys,os
import telnetlib

def check_port(host,port):
    check_port = telnetlib.Telnet()
    str_port = str(port)
    try:
        result = check_port.open(host,str_port)
        print result
        port_status = "The port is open!"
        return port_status
    except Exception as err:
        port_status = "The port is down!"
        return port_status
    finally:
        check_port.close()
