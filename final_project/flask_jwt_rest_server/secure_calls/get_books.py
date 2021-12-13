from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from db_con import get_db_instance, get_db
import sys
sys.path.append('..')

from tools.logging import logger
global_db_con = get_db()

def handle_request():
    logger.debug("Get Books Handle Request")
    return json_response( token = create_token(  g.jwt_data ) , pass_back = user_books ,books = {})
