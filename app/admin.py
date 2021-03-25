from flask.templating import render_template
from flask import Flask, render_template, redirect,url_for,request,flash,session,sessions
from app import app
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import pymysql
import re
from pymysql import cursors
from werkzeug.utils import format_string

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '123456'
# app.config['MYSQL_DB'] = 'cts'
# mysql = MySQL(app) 


# Function LOGOUT
@app.route('/logout')
def logout():
    session.pop('idname', None)
    return render_template("res.html")

# Function LAYOUT MENU
@app.route('/layout')
def layout():
    return render_template("layout.html")


# Đổi thưởng user
@app.route('/doithuonguser')
def doithuonguser():
    return render_template('exchange.html')

@app.route('/ax')
def ax():
    return render_template("res.html")