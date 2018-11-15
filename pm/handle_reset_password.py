#encoding:utf-8

import json
import sys,os

password = "password"

def jsonGet(site,port,username,ftx_admin_user):
    xget_command = r"curl -XGET http://" + site + ":" + port + "/rest/admin/user/users/" + username + " -u " + ftx_admin_user + ":" + password + " > curl_get.json"
    return xget_command
    # os.system(xget_command)

def userGet(username):
    user_file = open('users.txt','wb')
    user_file.truncate()
    user_file.write(username)
    user_file.close()

def changePassword(site,port,username,ftx_admin_user,newpassword):
    userGet(username)
    username = open('users.txt')
    for user in username.readlines():
        curl_get = jsonGet(site,port,user,ftx_admin_user)
        json_file = open(r'curl_get,json')
        context = json.load(json_file)
        context["password"] = newpassword
        change_json = json.dumps(context)
        xput_command = r"curl -XPUT http://" + site + ":" + port + "/rest/admin/user/users -u " + ftx_admin_user + ":" + password + " -d '" + change_json + "' -H 'Content-Type: application/json'"
        print xput_command


        # json_file = open(r'users.json')
        # context = json.load(json_file)