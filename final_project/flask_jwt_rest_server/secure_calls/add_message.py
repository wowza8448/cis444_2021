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
    message = request.args.get("chat")
    sqlInsert = """INSERT INTO userchats(username, chat) values(%s, %s);"""
    cur.execute(sqlInsert, (username, message))
    global_db_con.commit()
    return json_response()
