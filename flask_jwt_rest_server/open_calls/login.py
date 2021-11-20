from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from db_con import get_db_instance, get_db
import sys
sys.path.append('..')
import bcrypt

from tools.logging import logger
global_db_con = get_db()

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    username = request.form['firstname']
    password_from_user_form = request.form['password']
    cur = global_db_con.cursor()
    cur.execute("SELECT * FROM users WHERE username = username;")
    match = cur.fetchone()
    if match == None:
        return json_response(status_=401, message = 'Invalid credentials', authenticated = False)
    else:
        hash = match[1].encode('utf-8')
        new = bcrypt.checkpw(bytes(password_from_user_form, 'utf-8'), hash)
        if new == True:
            user = { "sub" : username } #sub is used by pyJwt as the owner of the token 
        else:
            return json_response(status_=401, message = 'Invalid credentials', authenticated = False)
    if not user:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )
    
    return json_response( token = create_token(user) , authenticated = True)

