from typing import ContextManager
from flask.globals import g
from flask.templating import render_template
from flask import Flask, render_template, redirect,url_for,request,flash,session,sessions
from app import app
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import pymysql
import re
import smtplib ,ssl
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from pymysql import cursors
from werkzeug.utils import format_string
import configadmin
from flask_mail import Mail,Message
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config.from_pyfile('config.cfg')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'cts'
mysql = MySQL(app) 
mail = Mail(app)
s = URLSafeTimedSerializer('thisisascrect!')
# app = Flask(__name__,template_folder='../app/templates')


#Chuc nang dang ky tai khoan
@app.route('/la')
def la():
    return render_template('form_mail.html')
@app.route('/Dang_ky',methods=['GET', 'POST'])
def Dang_ky():
    if request.method == 'GET':
        return render_template('res.html')
    email = request.form['email']
    token = s.dumps(email, salt ='email-confirm')
    #msg = Message('Confirm email', sender="hoangviet1807@gmail.com", recipients=[email])
    
    sender_email = "hoangviet1807@gmail.com"
    receiver_email = email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "multipart test" 
    msg["From"] = sender_email 
    msg["To"] = receiver_email 
    link = url_for('confirm_email', token = token, _external = True)
    text = """\ Hi, Check out the new post on the Mailtrap blog: SMTP Server for Testing: Cloud-based or Local? https://blog.mailtrap.io/2018/09/27/cloud-or-local-smtp-server/ Feel free to let us know what content would be useful for you!""" 
    html = render_template('form_mail.html')
    
    part1 = MIMEText(text,'plain')
    part2 = MIMEText(html,'html')

    msg.attach(part1)
    msg.attach(part2)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, "hoangviet01")
        server.sendmail(
        sender_email, receiver_email, msg.as_string()
    )
    return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)
   
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
@app.route('/change_pass', methods=['GET','POST'])
def change_pass():
    email = request.args.get('email', None)
    if request.method == 'POST':
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE employee SET password=%s WHERE email=%s", (password,email))
        mysql.connection.commit()
        return redirect(url_for('logi'))
    return render_template('update_password.html', email = email)


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
        value = request.form.getlist('check') 
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM employee WHERE email = %s AND password = %s', (tma, password,))
        account = cursor.fetchone()
        # idempl = account[0]

        if tma==configadmin.username and password==configadmin.password:
            session['idname'] = request.form['idname']  
            return render_template('/home.html')

        if account:
            session['idname'] = request.form['idname'] 
            tmaname = account[3]             
            return render_template('/home.html')

        else:
            loi = 'Tài khoản hoặc mật khẩu sai'
    return render_template("res.html",loi=loi)
    
#Function REGISTER 
@app.route('/regis',methods=['GET','POST'])
def signup():
    loi =""
    if request.method == 'POST':
        firt_name = request.form['first_name']
        last_name = request.form['last_name']
        name = firt_name+" "+last_name
        idname = request.form['idname']
        password = request.form['password']
        repassword = request.form['repassword']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        role = request.form['role']
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (idname,))
        account = cursor.fetchone()
        if account:
            loi = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', idname):
            loi = 'Id Name must contain only characters and numbers!'
        elif not idname or not password or not name or not address  or not city or not country or not role :
            loi = 'Please fill out the forma!'
        elif password !=repassword:
            loi = ' Comfirm password is wrong'
        else:
            cursor.execute('insert INTO  Account(NAME, IDNAME, PASSWORD,ADDRESS,CITY,COUNTRY,ROLE) VALUES (%s, %s, %s,%s,%s,%s,%s)',(name,idname,password,address,city,country,role,))
            mysql.connection.commit()
            loi = "Sign up succesfully"
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
         

#Function EDIT EMPLOYEE
@app.route('/edit',methods=["GET","POST"])
def edit():
    account=""
    succ = ""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account')
    account = cursor.fetchall()
    if request.method == 'POST':
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (tma,))
        acc = cursor.fetchone()
        flash("Welcome {}".format(acc[1]))
        id = request.form.get('id')
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        sql="UPDATE Account SET NAME=%s, ADDRESS=%s, CITY =%s, COUNTRY=%s WHERE IDNAME=%s and TT=%s"
        cursor.execute(sql,(name,address,city,country,id,acc[0]))
        if acc[2] == id:
            mysql.connection.commit()
            succ = "UPDATED SUCCESSFUL"
            cursor.execute('SELECT * FROM Account')
            account = cursor.fetchall()
            return render_template("employeeadmin.html",account=account,succ=succ)
        else:
            ac = "ONLY UPDATE YOUR INFORMATION"
            return render_template("employeeadmin.html",account=account,ac=ac)

# Add
@app.route('/add',methods=["GET","POST"])
def add():
    ac=""
    succ =""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account')
    account = cursor.fetchall()
    if request.method == 'POST':
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (tma,))
        acc1 = cursor.fetchone()
        firt_name = request.form['first_name']
        last_name = request.form['last_name']
        name = firt_name+" "+last_name
        idname = request.form['idname']
        password = request.form['password']
        repassword = request.form['repassword']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        select = request.form.get('selectrole')
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (idname,))
        acc = cursor.fetchone()
        flash("Welcome {}".format(tmaname))
        if acc1[7]!="ADMIN":
            ac = 'Only ADMIN ADD EMPLOYEE'
            cursor.execute('SELECT * FROM Account')
            account = cursor.fetchall()
        elif acc:
            ac = 'Account already exists!'
            cursor.execute('SELECT * FROM Account')
            account = cursor.fetchall()
        elif not re.match(r'[A-Za-z0-9]+', idname):
            ac = 'Id Name must contain only characters and numbers!'
            cursor.execute('SELECT * FROM Account')
            account = cursor.fetchall()
        elif not idname or not password or not name or not address  or not city or not country or not select :
            ac = 'Please fill out the form!'
            cursor.execute('SELECT * FROM Account')
            account = cursor.fetchall()
        elif password !=repassword:
            ac = ' Comfirm password is wrong'
            cursor.execute('SELECT * FROM Account')
            account = cursor.fetchall()
        else:
            cursor.execute('insert INTO  Account(NAME, IDNAME, PASSWORD,ADDRESS,CITY,COUNTRY,ROLE) VALUES (%s, %s, %s,%s,%s,%s,%s)',(name,idname,password,address,city,country,select,))
            mysql.connection.commit()
            succ = "Sign up username:"+ idname+" succesfully"
    return render_template("employeeadmin.html",account=account,succ=succ,ac=ac)
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
    cursor = mysql.connection.cursor()
    cursor.execute("select missionprocess.id_process, mission.id_mission, mission.name_mission\
        ,mission.describe,mission.startdate,mission.enddate , mission.point , \
        missionprocess.status  from employee, mission, missionprocess\
        where missionprocess.id_employee=employee.id_employee and \
        missionprocess.id_mission=mission.id_mission \
        and employee.email = %s",(tma,))
    x = cursor.fetchall()
    flash("Welcome {}".format(tmaname))
    return render_template('nhiemvuuser.html',x=x)
# Hoàn thành nhiệm vụ
@app.route('/done',methods=['GET','POST'])
def done():
    succ=""
    idprocess = request.form['idprocess']
    cursor = mysql.connection.cursor()
    cursor.execute("select missionprocess.id_process, mission.id_mission, mission.name_mission\
        ,mission.describe,mission.startdate,mission.enddate , mission.point , \
        missionprocess.status  from employee, mission, missionprocess\
        where missionprocess.id_employee=employee.id_employee and \
        missionprocess.id_mission=mission.id_mission \
        and employee.email = %s",(tma,))
    x = cursor.fetchall()

    cursor.execute("UPDATE missionprocess SET status = 'Hoàn thành' WHERE id_process = %s",(idprocess,))
    mysql.connection.commit()
    succ = "UPDATED SUCCESSFUL"

    flash("Welcome {}".format(tmaname))

    return render_template('nhiemvuuser.html',succ=succ,x=x)

# Chức năng nhận nhiệm vụ available
@app.route('/nhannhiemvu/<id>/',methods=['GET','POST'])
def nhannhiemvu(id):
    cursor = mysql.connection.cursor()
    a = 1
    sta = "dang lam"
    # cursor.execute=('INSERT INTO missionprocess (id_employe, id_mission, status) \
    # VALUES (%s,%s,%s)',(a,id,sta))
    cursor.execute('INSERT INTO `cts`.`missionprocess` (`id_employee`, `id_mission`, `status`) \
VALUES (%s,%s,%s)',(1,id,sta,))
    
    if request.method == "GET":
        mysql.connection.commit()
        succ =str(id) + sta 
        return render_template('nhiemvuuser1.html',succ=succ)

@app.route('/nhiemvuuser1',methods=['GET','POST'])
def nhiemvuuser1():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM mission')
    account = cursor.fetchall()
    # flash("Welcome {}".format(tmaname))

    return render_template('nhiemvuuser1.html',account=account)


# Thông tin cá nhân user
@app.route('/canhanuser')
def canhanuser():
   
    return render_template('editprofile.html')

app.run(debug=True)


