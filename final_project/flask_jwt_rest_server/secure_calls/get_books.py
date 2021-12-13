from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from db_con import get_db_instance, get_db
import sys
sys.path.append('..')

from tools.logging import logger
global_db_con = get_db()

def handle_request():
    cur = global_db_con.cursor()
    username = g.jwt_data['sub']
    sqlExecute = "SELECT * from userchats"
    cur.execute(sqlExecute)
    rows = cur.fetchall()
    if rows == None:
        return "Chat is empty"
    else:
        lst = []
        for row in rows:
            lst.append(row[1])
        user_books = str(lst)
        print(user_books)
    return json_response( token = create_token(  g.jwt_data ), pass_back = user_books, books = {})
