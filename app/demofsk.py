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
import hashlib,uuid



app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
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
        passhash = hashlib.md5(password.encode()).hexdigest()
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM employee WHERE email = %s AND password = %s', (tma,  passhash,))
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
    # flash("Welcome {}".format(name))
    return render_template('nhiemvuuser1.html',account=account)


# Thông tin cá nhân user
@app.route('/canhanuser')
def canhanuser():
    cursor = mysql.connection.cursor()
    cursor.execute("Select * from cts.employee where email = %s",(session['idname'],))
    employee = cursor.fetchall()
    return render_template('editprofile.html',employee = employee,data=[{'name':'Nam'},{'name':'Nữ'}])

# cập nhập tin cá nhân user
@app.route('/capnhat', methods =["POST"])
def capnhat():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        
        hoten = request.form['edithoten']
        diachi = request.form['editdiachi']
        ngaysinh = request.form['editngaysinh']
        sodt = request.form['editsodt']
        chucvu = request.form['editchucvu']
        gioitinh = request.form['select']
        cursor.execute("Update cts.employee set name_employ = %s,address = %s, birthday=%s,deparment=%s,phonenumber=%s,\
        gender=%s where email = %s",(hoten,diachi,ngaysinh,chucvu,sodt,gioitinh,session['idname']))
        mysql.connection.commit()
        flash("Cập Nhật Thành Công")

    return redirect(url_for('canhanuser'))



@app.route('/la')
def la():
    return render_template('form_mail.html')
@app.route('/Dang_ky', methods=['GET', 'POST'])
def Dang_ky():
    loidk = ""
    if request.method == 'POST':
        email = request.form['email']
        token = s.dumps(email, salt='email-confirm')
        #msg = Message('Confirm email', sender="hoangviet1807@gmail.com", recipients=[email])
        sender_email = "holongk15@gmail.com"
        receiver_email = email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Link Confirm"
        msg["From"] = sender_email
        msg["To"] = receiver_email
        link = url_for('confirm_email', token=token, _external=True)
        text = """\Hi """
        html = render_template('form_mail.html', link=link, email=email)
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM Employee WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            loidk = "Tài khoản này đã tồn tại"
        else:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, "hoxuanlong12345")
                server.sendmail(
                    sender_email, receiver_email, msg.as_string().encode('utf-8')
                )
                return render_template('noti_res.html')
        # return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)
    return render_template('res.html', loidk = loidk)



#Chức năng xác nhận link confirm gmail
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=36000)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee (email) VALUES (%s)", (email,))
        mysql.connection.commit()
        return redirect(url_for('change_pass', email = email))
    except SignatureExpired:
        return '<h1> The token is expired </h1>' 

#Chức năng update mật khẩu

@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
  
    loi = ""
    email = request.args.get('email', None)
    if request.method == 'POST':
        password = request.form['password']
        pass_confirm = request.form['pass_confirm']
        
        if password != pass_confirm:
            loi = "Mật khẩu không khớp"
        else:
            
            cur = mysql.connection.cursor()
            hashpass = hashlib.md5(password.encode('utf-8')).hexdigest()
            cur.execute("UPDATE employee SET password=%s WHERE email=%s",
                        (hashpass, email))
            mysql.connection.commit()
           
            session['idname'] = email
            

            return render_template('/home.html', email = email)
    return render_template('update_password.html', email=email, loi = loi)
app.run(debug=True)
