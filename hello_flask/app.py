from flask import Flask,render_template,request, redirect, url_for, session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from functools import wraps

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

@app.route('/getBooks', methods = ["GET", "POST"])
def books():
    token = session['token']
    isValid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    timeCheck = datetime.timedelta(minutes=30)
    if isValid['username'] != None:
        return redirect('/static/books.html')
    else:
        return "Invalid token"
    

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
            if new == True:
                token = JWT_Token(username)
                session['token'] = token
                return redirect('/getBooks')
            else:
                return "Invalid login"
    return "Error"

def JWT_Token(user):
    payload = list(user)
    token = jwt.encode({'username': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return token

@app.route('/buy', methods = ["GET", "POST"])
def buy():
    if request.method == "POST":    
        newBook = ""
        cur = global_db_con.cursor()
        if request.form.get('horton'):
            newBook = "horton"
        elif request.form.get('grinch'):
            newBook = "the grinch"
        sqlInsert = """INSERT INTO booksOwned(username, book) values(%s, %s);"""
        token = session['token']
        jwt_key = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = jwt_key['username']
        print(username)
        cur.execute(sqlInsert, (username, book))

        return "book purchased"

@app.route('/addUser', methods = ["GET", "POST"])
def addUser():
    if request.method == "POST":
        cur = global_db_con.cursor()
        username1 = request.form.get("username")
        password = request.form.get("password")
        password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
        password = password.decode('utf-8')
        sqlInsert = """INSERT INTO users(username, password) values(%s, %s);"""
        cur.execute(sqlInsert,(username1, password))
        global_db_con.commit()
        print("User created")
        return "User " + username1 + " created!"
    return "Something went wrong"


#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )


app.run(host='0.0.0.0', port=80)

