from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager

SECRET_KEY = 'so-so-so-so-so-difficult-key'
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datebase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    mail = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_type = db.Column(db.String(50), default='anonim')

    def __repr__(self):
        return '<Users %r' % self.id


class LoginForm:
    validate_on_submit = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(15), primary_key=True, nullable=False)
    password = db.Column(db.String(500), nullable=True)
    remember_me = db.Column(db.String(5), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/s-u')
def Sign_up():
    return render_template('base.html')


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
