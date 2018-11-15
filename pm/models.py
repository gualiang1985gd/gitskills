#encoding:utf-8

from exts import db
from datetime import datetime,date
from werkzeug.security import generate_password_hash,check_password_hash

class User():
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    groupname = db.Column(db.String(20),nullable=False)
    userstatus = db.Column(db.String(30),nullable=False,default='启用')

    def __init__(self,*args,**kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        groupname = kwargs.get('groupname')
        self.username = username
        self.password = generate_password_hash(password)
        self.groupname = groupname

    def check_password(self,raw_password):
         result = check_password_hash(self.password,raw_password)
         return result

class ServersInfo(db.Model):
    __tablename__ = 'serversinfo'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    server_name = db.Column(db.String(50),nullable=False)
    wan_ip = db.Column(db.String(20))
    ssh_port = db.Column(db.String(10))
    username = db.Column(db.String(20))
    password = db.Column(db.String(30),nullable=False)
    log_path = db.Column(db.Text(100))
