from flask.templating import render_template
from flask import Flask, render_template, redirect,url_for,request,flash,session,sessions

from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import pymysql
import re
from pymysql import cursors
from flask_paginate import Pagination, get_page_parameter
from werkzeug.utils import format_string


app = Flask(__name__,template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'Company'
mysql = MySQL(app) 


# @app.route('/template')
# def temp():
#     return render_template('template.html')

@app.route('/haha')
def demo():
    return render_template('tmahome.html')

# Function HOME
@app.route('/',methods=['GET','POST'])
def index():
    if 'idname' in session:
        idname = session['idname']
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (idname,))
        account = cursor.fetchone()
        flash("Welcome {}".format(account[1]))
        return render_template('home.html')
    return render_template('logi.html')
    # if session.get('loggedin')==True:
    #      return "Hello Boss!"
 
# Function logi
@app.route('/logi',methods=['GET','POST'])
def logi():
    loi = None
    if request.method == 'POST':
        idname = request.form['idname']
        password = request.form['password']
        value = request.form.getlist('check') 
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s AND PASSWORD = %s', (idname, password,))
        account = cursor.fetchone()
        # Check account and remember save in session
        if account and value == [u'check']:
            session['idname'] = request.form['idname']
            flash("Welcome {}".format(account[1]))
            return render_template('/home.html')
            # Redirect to home page
        # Check remember not save in session
        elif account:
            flash("Welcome {}".format(account[1]))
            return render_template('/home.html')
        else:
            loi = 'Incorrect idname/password!'
    return render_template("logi.html",loi=loi)
    
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
            loi = 'Please fill out the form!'
        elif password !=repassword:
            loi = ' Comfirm password is wrong'
        else:
            cursor.execute('insert INTO  Account(NAME, IDNAME, PASSWORD,ADDRESS,CITY,COUNTRY,ROLE) VALUES (%s, %s, %s,%s,%s,%s,%s)',(name,idname,password,address,city,country,role,))
            mysql.connection.commit()
            loi = "Sign up succesfully"
    return render_template("regis.html",loi=loi)


# Function LOGOUT
@app.route('/logout')
def logout():
    session.pop('idname', None)
    return render_template("logi.html")

# Function LAYOUT
@app.route('/layout')
def layout():
    return render_template("layout.html")

# Function HOME
@app.route('/home',methods=['GET'])
def home():
    return render_template("home.html")


# Function EMPLOYEE
@app.route('/employee',methods=['GET','POST'])
def employee():
    cursor = mysql.connection.cursor() 
    cursor.execute('SELECT * FROM Account')
    account = cursor.fetchall()
    if 'idname' in session:
        idname = session['idname'] 
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (idname,))
        acc = cursor.fetchone()
        flash("Welcome {}".format(acc[1]))
        return render_template("template.html",account=account)
    elif 'idname' not in session:
        flash("Welcome TMA SOLUTON")
        return render_template("template.html",account=account)

#Function VIEW EMPLOYEE
@app.route('/view/<id>/',methods=["GET","POST"])
def view(id):
    succ=""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account')
    account = cursor.fetchall()
    if 'idname' in session:
        idname = session['idname'] 
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (idname,))
        acc = cursor.fetchone()
        flash("Welcome {}".format(acc[1]))
        succ = id
        return render_template("template.html",succ=succ,account=account)
    elif 'idname' not in session:
        cursor.execute('SELECT * FROM Account')
        account = cursor.fetchall()
        flash("Welcome TMA SOLUTON")
        succ = id
        return render_template("template.html",succ=succ,account=account)


#Function DELETE EMPLOYEE
@app.route('/delete/<id>/',methods=["GET","POST"])
def delete(id):
    account=""
    succ = ""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account')
    account = cursor.fetchall()
    if 'idname' in session:
        idname = session['idname'] 
        aa = id
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (idname,))
        acc = cursor.fetchone()
        flash("Welcome {}".format(acc[1]))
        if int(acc[0]) == int(id):
            ac= "Can't delete yourself"
            return render_template("template.html",account=account,ac=ac)
        elif acc[7]=="ADMIN":
            cursor = mysql.connection.cursor()
            cursor.execute('DELETE FROM Account WHERE TT=%s',(id,))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM Account')
            account = cursor.fetchall()
            succ = "DELETE " + id + " SUCCESSFUL"
            return render_template("template.html",account=account,succ=succ)
        else:
            cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (idname,))
            ac = "Only ADMIN DELTE"
            return render_template("template.html",account=account,ac=ac)
         
    elif 'idname' not in session:
        flash("Welcome TMA SOLUTION")
        ac = "PLEASE SAVE SESSION TO ACTION"
        return render_template("template.html",account=account,ac=ac)

#Function EDIT EMPLOYEE
@app.route('/edit',methods=["GET","POST"])
def edit():
    account=""
    succ = ""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account')
    account = cursor.fetchall()
    if request.method == 'POST':
        if 'idname' in session:
            idname = session['idname'] 
            cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (idname,))
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
                return render_template("template.html",account=account,succ=succ)
            else:
                ac = "ONLY UPDATE YOUR INFORMATION"
                return render_template("template.html",account=account,ac=ac)
        elif 'idname' not in session:
            flash("Welcome TMA SOLUTION")
            ac = "PLEASE SAVE SESSION TO ACTION"
            return render_template("template.html",account=account,ac=ac)


# Search employee
# @app.route('/search',methods=["GET","POST"])
# def search():
#     succ=""
#     account=""
#     search = "%"+request.form['search']+"%"
#     cursor = mysql.connection.cursor()
#     sql = "SELECT * FROM Account where NAME LIKE %s or ADDRESS LIKE %s or CITY LIKE %s or COUNTRY LIKE %s or ROLE LIKE %s"
#     cursor.execute(sql,(search,search,search,search,search))
#     account = cursor.fetchall()
#     if 'idname' in session:
#         idname = session['idname'] 
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT * FROM Account WHERE IDNAME = %s', (idname,))
#         acc = cursor.fetchone()
#         flash("Welcome {}".format(acc[1]))
#     elif 'idname' not in session:
#         flash("Welcome to TMA SOLUTONS")
#     return render_template("template.html",succ=succ,account=account)

@app.route('/add',methods=["GET","POST"])
def add():
    ac=""
    succ =""
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Account')
    account = cursor.fetchall()
    if request.method == 'POST':

        if 'idname' in session:
            idname1 = session['idname'] 
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
            flash("Welcome {}".format(acc[1]))
            if idname1!="TMA1":
                ac = 'Only ADMIN ADD EMPLOYEE'
                cursor.execute('SELECT * FROM Account')
                account = cursor.fetchall()
            elif account:
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
            
    return render_template("template.html",account=account,succ=succ,ac=ac)
            
@app.route('/pagi',methods=["GET","POST"])
def pani():
    return render_template("pagination.html")
app.run(debug=True)


