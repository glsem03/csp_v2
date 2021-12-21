from flask import Flask
import os
import sqlite3

DATABASE = '/'
DEBUG = True
SECRET_KEY = 'CAJhjasklGUgklA<4%^g,b.jgvnb'
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():  # put application's code here
    return 'Hello World!'


@app.route('/about')
def about():
    return 'About'


if __name__ == '__main__':
    app.run(debug=True)
