from flask.templating import render_template
from flask import Flask, render_template, redirect,url_for,request,flash,session,sessions
from app import app
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import pymysql
import re
from pymysql import cursors
from werkzeug.utils import format_string


# # app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '123456'
# app.config['MYSQL_DB'] = 'cts'
# mysql = MySQL(app) 

@app.route('/a',methods=['GET','POST'])
def h():
    return render_template("home.html")

@app.route('/nhiemvuuser',methods=['GET','POST'])
def ha1():
    return render_template("nhiemvuuser.html")
