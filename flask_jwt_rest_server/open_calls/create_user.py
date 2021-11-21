from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from db_con import get_db_instance, get_db
import sys
sys.path.append('..')
import bcrypt

global_db_con = get_db()

def handle_request():
    username = request.form['2firstname']
    password = request.form['2password']
    password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    password = password.decode('utf-8')
    cur = global_db_con.cursor()
    sqlInsert = """INSERT INTO users(username, password) values(%s, %s);"""
    cur.execute(sqlInsert,(username, password))
    global_db_con.commit()
    return json_response()
