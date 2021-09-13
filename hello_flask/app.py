from flask import Flask

app = Flask(__name__)


USER_PASSWORDS = { "cjardin": "strong password"}


@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

app.run(host='0.0.0.0', port=80)

