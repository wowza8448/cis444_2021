from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json

import jwt
import datetime
import bcrypt

from db_con import get_db_instance, get_db

app = Flask(__name__)



USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    return render_template('backatu.html',username = str(request.form['username']) )


#Assignment 3
@app.route('/getUser', methods =["GET", "POST"])
def getUser():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        return "Welcome " + username
    return render_template("first_form.html")

#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )


app.run(host='0.0.0.0', port=80)

