from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from db_con import get_db_instance, get_db
import sys
sys.path.append('..')

global_db_con = get_db()

def handle_request():
    username = g.jwt_data['sub']
    cur = global_db_con.cursor()
    newBook = "Horton Hears a Who"
    sqlInsert = """INSERT INTO booksOwned(username, book) values(%s, %s);"""
    cur.execute(sqlInsert, (username, newBook))
    global_db_con.commit()
    return json_response()
    
