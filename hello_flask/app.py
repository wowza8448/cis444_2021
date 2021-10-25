from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json

import jwt
import datetime
import bcrypt

from db_con import get_db_instance, get_db

app = Flask(__name__)

JWT_SECRET = None


USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
global_db_con = get_db()

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

app.config['SECRET_KEY'] = 'supersecretkey'


@app.route('/getUser', methods =["GET", "POST"])
def getUser():
    if request.method == "POST":
        cur = global_db_con.cursor()
        username = request.form.get("username")
        password = request.form.get("password")
        cur.execute("SELECT * FROM users WHERE username = username;")
        match = cur.fetchone()
        if match == None:
            return "Invalid login"
        else:
            hash = match[1].encode('utf-8')
            new = bcrypt.checkpw(bytes(password, 'utf-8'), hash)
            if True:
                return "Login accepted"
            else:
                return "Invalid login"
    return render_template("first_form.html")

@app.route('/addUser', methods = ["GET", "POST"])
def addUser():
    if request.method == "POST":
        cur = global_db_con.cursor()
        username1 = request.form.get("username")
        password = request.form.get("password")
       # payload = list(password)
       # password1 = jwt.encode({'password': password}, app.config['SECRET_KEY'])
        password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
        password = password.decode('utf-8')
        print(password)
        sqlInsert = """INSERT INTO users(username, password) values(%s, %s);"""
        cur.execute(sqlInsert,(username1, password))
        global_db_con.commit()
        print("User created")
        return "User " + username1 + " created!"
    return render_template("second_form.html")


#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )


app.run(host='0.0.0.0', port=80)

