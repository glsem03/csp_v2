from flask import Flask
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager

DATABASE = '/'
DEBUG = True
SECRET_KEY = 'CAJhjasklGUgklA<4%^g,b.jgvnb'
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///nkedb.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    mail = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_type = db.Column(db.String(50), default='student')


@app.route('/')
def Login():  # put application's code here
    return 'Страница входа'


@app.route('/main')
def Main():
    return 'Основная страница'


@app.route('/schedule')
def Schedule():
    return 'Расписание'


@app.route('/teachers')
def Teachers():
    return 'Учителя'


if __name__ == '__main__':
    app.run(debug=True)
