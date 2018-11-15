#encoding:utf-8
import json
import sys,os

def read_json():
    with open(r"users.json",'r')as load_f:
        load_dict = json.load(load_f)
        username = load_dict["username"]
        password = load_dict["password"]
        group = load_dict["group"]
        status = load_dict["status"]
        load_f.close()
    return username,password,group,status

def read_db_json_indices():
    with open(r"db.json",'r')as read_db_f:
        load_dict = json.load(read_db_f)
        db_info = load_dict
        # for db in db_info:
    return db_info


def write_db_json(after):
    with open(r"db.json",'wb')as write_db_f:
        json.dump(after,write_db_f)
        # write_db_f.write(after)
        write_db_f.close()