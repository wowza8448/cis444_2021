from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from db_con import get_db_instance, get_db
import sys
sys.path.append('..')

global_db_con = get_db()

def handle_request():
    print("Add friend")
    return json_response()
