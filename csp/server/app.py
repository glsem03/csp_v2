import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, g, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# !config info!
SECRET_KEY = 'so-so-so-so-so-difficult-key'
DATABASE = '/csp/server/database.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))

db = SQLAlchemy(app)
login_manager = LoginManager(app)


#  проверка соединения с бд
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


#  создание базы, если она отсутсвует
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


#  соединение с бд
def get_db():
     if not hasattr(g, 'link_db'):
         g.link_db = connect_db()

     return g.link_db


#  разрыв соединения
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login = db.Column(db.String(50), nullable=False, primary_key=True)
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Anonim')

    marks = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Users %r' % self.id


class LoginForm(db.Model):
    validate_on_submit = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(15), primary_key=True, nullable=False)
    password = db.Column(db.String(500), nullable=True)
    remember_me = db.Column(db.String(5), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)


@app.route('/', methods=['POST', 'GET'])
def Login():

    username = request.form['username']
    password = request.form['password']

    if 'userLogged' in session:
        return redirect((url_for('main', username=session['userLogged'])))

    if request.method == "POST":
        if request.form['username'] in db:
            session['userLogged'] = request.form['username']
            return redirect(url_for('main', username=session['userLogged']))
        else:

            login_form = LoginForm(validate_on_submit='None', username=str(username), password=str(password), remember_me='Yes')

            try:
                db.session.add(login_form)
                db.session.commit()
                return redirect('/main')

            except:
                return "Что-то сделанно не правильно"

    return render_template('authorization.html')


@app.route('/main/<username>')
def personal_page(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    else:
        return f'profile of userv{username}'


@app.route('/main')
def Main():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template('index.html', Users=Users.query.all())


@app.route('/schedule')
def Schedule():
    return 'Расписание'


@app.route('/teachers')
def Teachers():
    return 'Учителя'


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Станица не найдена :(')


if __name__ == '__main__':
    app.run(debug=True)
