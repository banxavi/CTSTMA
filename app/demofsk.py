from typing import ContextManager
from flask.globals import g
from flask.templating import render_template
from flask import Flask, render_template, redirect, url_for, request, flash, session, sessions
from app import app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql
import re
import smtplib
import ssl
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from pymysql import cursors
from werkzeug.utils import format_string
import configadmin
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'cts'
mysql = MySQL(app) 
mail = Mail(app)
s = URLSafeTimedSerializer('thisisascrect!')


# app = Flask(__name__,template_folder='../app/templates')

# Function HOME
@app.route('/',methods=['GET','POST'])
def index():
    global email
    global name 
    global idplo
    if session['idname'] =="abc":
        return render_template('home.html')

    elif 'idname' in session: 
        email= session['idname']
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM employee WHERE email = %s', (email,))
        table = cursor.fetchone()
        name = table[3]
        idplo = table[0]
        return render_template('home.html', name=name,idname = email)
   
    else:
        return render_template('res.html')

@app.route('/home',methods=['GET','POST'])
def ha():
    if 'idname' in session: 
        return render_template('home.html')
    else:
        return render_template('res.html')

    

# Function logi
@app.route('/logi',methods=['GET','POST'])
def logi():
    loi = None
    global tmaname
    global tma
    global idempl
    # try:
    if request.method == 'POST':
        tma = request.form['idname']
        password = request.form['password']
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM employee WHERE email = %s AND password = %s', (tma, password,))
        account = cursor.fetchone()

        if tma==configadmin.username and password==configadmin.password:
            session['idname'] = request.form['idname']  
            return render_template('/home.html' )

        if account:
            session['idname'] = request.form['idname']      
            return render_template('/home.html')

        else:
            loi = 'Tài khoản hoặc mật khẩu sai'
    return render_template("res.html",loi=loi)
    



# Function EMPLOYEE MANAGEMENT
@app.route('/employee',methods=['GET','POST'])
def employee():
    cursor = mysql.connection.cursor() 
    cursor.execute('SELECT * FROM employee')
    account = cursor.fetchall()
    a = 1
    cursor.execute('select mission.id_mission, employee.name_employ, mission.name_mission , mission.point , missionprocess.status  from \
    employee, mission, missionprocess \
    where missionprocess.id_employee=employee.id_employee and missionprocess.id_mission=mission.id_mission \
    and  employee.id_employee=%s',(a,))
    x = cursor.fetchall()
    return render_template("employeeadmin.html",account=account,x=x)


#Function VIEW EMPLOYEE
@app.route('/view/<id>/',methods=["GET","POST"])
def view(id):
    succ=""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account')
    account = cursor.fetchall()

    cursor = mysql.connection.cursor()
    succ = id
    return render_template("employeeadmin.html",succ=succ,account=account)

#Function DELETE EMPLOYEE
@app.route('/delete/<id>/',methods=["GET","POST"])
def delete(id):
    account=""
    succ = ""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account')
    account = cursor.fetchall()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (tma,))
    acc = cursor.fetchone()
    flash("Welcome {}".format(acc[1]))
    if int(acc[0]) == int(id):
        ac= "Can't delete yourself"
        return render_template("employeeadmin.html",account=account,ac=ac)
    elif acc[7]=="ADMIN":
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Account WHERE TT=%s',(id,))
        mysql.connection.commit()
        cursor.execute('SELECT * FROM Account')
        account = cursor.fetchall()
        succ = "DELETE " + id + " SUCCESSFUL"
        return render_template("employeeadmin.html",account=account,succ=succ)
    else:
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (tma,))
        ac = "Only ADMIN DELTE"
        return render_template("employeeadmin.html",account=account,ac=ac)
         

#Function EDIT nhiệm vụ
@app.route('/editnhiemvu',methods=["GET","POST"])
def edit():

    account=""
    succ = ""
    cursor = mysql.connection.cursor()
  
    # cursor.execute('SELECT * FROM mission')
    # account = cursor.fetchall()

    id = request.form['id']
    namenv = request.form['name']
    mota = request.form["mota"]
    ngaybd = request.form['ngaybd']
    ngaykt = request.form['ngaykt']
    diem = request.form['diem']
    soluong = request.form['soluong']
    trangthai = request.form['trangthai']
                
    cursor.execute('update mission set name_mission=%s , startdate=%s, enddate = %s , point=%s, mota=%s, state=%s,sum_mission=%s \
        where id_mission=%s', (namenv,ngaybd,ngaykt,diem,mota,trangthai,soluong,id,))
    mysql.connection.commit()
    succ = "UPDATED SUCCESSFUL"
    return render_template("missionadmin.html",succ=succ)
# Add nhiệm vụ
@app.route('/addnhiemvu',methods=["GET","POST"])
def add():
   
    succ =""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM mission')
    account = cursor.fetchall()
    if request.method == 'POST':
        namenv = request.form['namenvu']
        mota = request.form['mota']
        ngaybd = request.form['ngaybd']
        ngaykt = request.form['ngaykt']
        diem = request.form['diem']
        soluong = request.form['soluong']
        trangthai = request.form.get('trangthai')
        
        cursor.execute('insert INTO  mission\
            (`name_mission`, `startdate`, `enddate`, `point`, `mota`, `state`, `sum_mission`) \
                VALUES (%s, %s, %s,%s,%s,%s,%s)',\
                    (namenv,ngaybd,ngaykt,diem,mota,trangthai,soluong,))
        mysql.connection.commit()
        succ = "Thêm thành công"
        return render_template("missionadmin.html",account=account,succ=succ)
# Mission Management
@app.route('/nhiemvu',methods=['GET','POST'])
def nhiemvu():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM mission')
    account = cursor.fetchall()
    return render_template('missionadmin.html',account=account)

# Reward Management
@app.route('/doithuong',methods=['GET','POST'])
def doithuong():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM exchange')
    account = cursor.fetchall()
    return render_template('rewardadmin.html',account=account)

# Danh sách nhiệm vụ user

@app.route('/nhiemvuuser',methods=['GET','POST'])
def nhiemvuuser():
    if 'idname' in session: 
        email= session['idname']
        cursor = mysql.connection.cursor()
        cursor.execute("select missionprocess.id_process, mission.id_mission, mission.name_mission\
            ,mission.mota,mission.startdate,mission.enddate , mission.point , \
            missionprocess.status  from employee, mission, missionprocess\
            where missionprocess.id_employee=employee.id_employee and \
            missionprocess.id_mission=mission.id_mission \
            and employee.email = %s",(email,))
        x = cursor.fetchall()
        
        cursor.execute('SELECT * FROM employee WHERE email = %s', (email,))
        table = cursor.fetchone()
        name = table[3]
        flash("Welcome {}".format(name))
        return render_template('nhiemvuuser.html',x=x)
  
       
# Hoàn thành nhiệm vụ
@app.route('/done',methods=['GET','POST'])
def done():
    succ=""
    idprocess = request.form['idprocess']
    cursor = mysql.connection.cursor()
    cursor.execute("select missionprocess.id_process, mission.id_mission, mission.name_mission\
        ,mission.mota,mission.startdate,mission.enddate , mission.point , \
        missionprocess.status  from employee, mission, missionprocess\
        where missionprocess.id_employee=employee.id_employee and \
        missionprocess.id_mission=mission.id_mission \
        and employee.email = %s",(email,))
    x = cursor.fetchall()

    cursor.execute("UPDATE missionprocess SET status = 'Hoàn thành' WHERE id_process = %s",(idprocess,))
    mysql.connection.commit()
    succ = "UPDATED SUCCESSFUL"

    flash("Welcome {}".format(name))

    return render_template('nhiemvuuser.html',succ=succ,x=x)

# Chức năng nhận nhiệm vụ available
@app.route('/nhannhiemvu/<id>/',methods=['GET','POST'])
def nhannhiemvu(id):
    cursor = mysql.connection.cursor()
    sta = "Đang làm"
    cursor.execute('INSERT INTO `cts`.`missionprocess` (`id_employee`, `id_mission`, `status`) \
VALUES (%s,%s,%s)',(idplo,id,sta,))

    cursor.execute('UPDATE mission SET sum_mission=sum_mission-1 where id_mission=%s',(id,))
    if request.method == "GET":
        mysql.connection.commit()
        succ =str(id) + sta 

        return render_template('nhiemvuuser1.html',succ=succ)

@app.route('/nhiemvuuser1',methods=['GET','POST'])
def nhiemvuuser1():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM mission')
    account = cursor.fetchall()
    flash("Welcome {}".format(name))
    return render_template('nhiemvuuser1.html',account=account)


# Thông tin cá nhân user
@app.route('/canhanuser')
def canhanuser():
    return render_template('editprofile.html')
app.run(debug=True)
