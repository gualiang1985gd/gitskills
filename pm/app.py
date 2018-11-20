#encoding:utf-8
import config
import os,sys
import json
import re
from flask import Flask,render_template,request,session,redirect,g,url_for
from decorators import login_required
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash,check_password_hash
from check_port_status import check_port
from handle_reset_password import jsonGet,changePassword
from readJson import read_json,read_db_json_indices,write_db_json

from linux_commands import check_server
from config import data_import_others,date_import_staging
# import flask_restful
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
# @login_required
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        #判断用户名和密码正确
        read_json()
        # user = User.query.filter(User.username == username).first()
        json_username,json_password,json_group,json_status = read_json()
        if username == json_username:
            if json_status == u'disable':
                return render_template('login.html',m=u'The user has been disabled')
            else:
                json_status == u"enable"
                groupname = json_group
                if json_username and check_password_hash(json_password,password):
                    session['user_user'] = json_username
                    #如果想在31天内都不需要登录
                    session.permanent = True
                    if groupname == u'admin':
                        return redirect(url_for('index'))
                else:
                    return render_template('login.html',m=u'The password is incorrect.Please check it before logging in.')
        else:
            return render_template('login.html',m=u'User does not exist')

@app.route('/resetpassword',methods=['GET','POST'])
@login_required
def reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html')
    if request.method == 'POST':
        adminuser = request.form.get('admin_user')
        site = request.form.get('site')
        port = request.form.get('port')
        newpassword = request.form.get('newpassword')
        username = request.form.get('userslist')
        # print site,port,newpassword,userslist
        message = check_port(host='127.0.0.1',port=port)
        # check_port = batch_reset_password(adminuser=adminuser,site=site,port=port,newpassword=newpassword,userslist=userslist)
        if message == 'The port is down!':
            return render_template('reset_password.html',m=message)
        else:
            changePassword(site,port,username,adminuser,newpassword)
            message = "App user password reset completed!"
            return render_template('reset_password.html',m=message)

@app.route('/importserverselect',methods=['GET','POST'])
@login_required
def import_server_select():
    if request.method == 'GET':
        return render_template('import_server_select.html')
    if request.method == 'POST':
        site = request.form.get('site')
        return render_template('data_import.html',site=site)

@app.route('/dataimport',methods=['GET','POST'])
@login_required
def data_import():
    if request.method == 'GET':
        return render_template('data_import.html')
    if request.method == 'POST':
        return render_template('import_server_select.html')

@app.route('/dbinfo',methods=['GET','POST'])
@login_required
def db_info():
    if request.method == 'GET':
        db_info = read_db_json_indices()
        details = { "db_info":db_info }
        return render_template('db_info.html',**details)

@app.route('/searchdbinfo',methods=['GET','POST'])
@login_required
def search_db_info():
    if request.method == 'GET':
        return redirect(url_for('db_info'))
    else:
        q = request.form.get('q')
        db_json = read_db_json_indices()
        for i in range(len(db_json)):
            for value in db_json[i].values():
                if q in value:
                    db_data = [db_json[i]];
                    details = { "db_info":db_data }
                    print db_json[i]
        return render_template('db_info.html',**details)

@app.route('/modifydbinfo',methods=['GET','POST'])
@login_required
def modify_db_info():
    if request.method == 'GET':
        number = request.args.get('number')
        site = request.args.get('site')
        sid = request.args.get('sid')
        username = request.args.get('username')
        password = request.args.get('password')
        login_status = request.args.get('login_status')
        null = request.args.get('null')
        create_table_permission = request.args.get('create_table_permission')
        return render_template('modify_db_info.html',number=number,site=site,sid=sid,username=username,password=password,login_status=login_status,null=null,create_table_permission=create_table_permission)
    if request.method == 'POST':
        i = 0
        db_json = read_db_json_indices()
        db_number = request.form.get('number')
        for i in range(len(db_json)):
            if db_json[i]["number"] == db_number:
                db_json[i]["site"] = request.form.get('site')
                db_json[i]["sid"] = request.form.get('sid')
                db_json[i]["username"] = request.form.get('username')
                db_json[i]["password"] = request.form.get('password')
                db_json[i]["login_status"] = request.form.get('login_status')
                db_json[i]["null"] = request.form.get('null')
                db_json[i]["create_table_permission"] = request.form.get('create_table_permission')
                write_db_json(db_json)
                return redirect(url_for('db_info'))

@app.route('/pagejump')
@login_required
def page_jump():
    return render_template('page_jump.html')

@app.before_request
def my_before_request():
    user_user = session.get('user_user')
    json_username = read_json()
    if user_user:
        user = json_username
        if user:
            g.user = user

if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    socketio.run(app,host='0.0.0.0',debug=True,port=5001)