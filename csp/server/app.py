import os
from flask import Flask, render_template, request, redirect, url_for, g, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, login_user, login_required, UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

# !config info!
SECRET_KEY = 'so-so-so-so-so-difficult-key'
DATABASE = '/csp/server/nkedb.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nkedb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'nkedb.db')))

db = SQLAlchemy(app)

login_manager = LoginManager(app)


class UserTypes(db.Model):
    __tablename__ = 'UserTypes'
    RoleId = db.Column(db.Integer(), unique=True, primary_key=True)
    RoleName = db.Column(db.Integer(), nullable=False)


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    UserId = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    UserLogin = db.Column(db.Text(), nullable=False)
    UserPassword = db.Column(db.Text(), nullable=False)
    UserTypeId = db.Column(db.Integer(), ForeignKey('UserTypes.RoleId'), nullable=False)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.UserId

    def __repr__(self):
        return '<UserLogin %r>' % (self.UserLogin)


class Groups(db.Model):
    __tablename__ = 'Groups'
    Id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    Name = db.Column(db.Text(), nullable=False)
    ElderId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)
    TeacherId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)


class GroupsToUsers(db.Model):
    __tablename__ = 'GroupsToUsers'
    Id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    UserId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)
    GroupId = db.Column(db.Integer(), ForeignKey('Groups.Id'), nullable=False)


class HomeWorkList(db.Model):
    __tablename__ = 'HomeWorkList'
    Id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    LessonId = db.Column(db.Integer(), ForeignKey('Lessons.Id'), nullable=False)
    HomeWorkDesc = db.Column(db.Text())


class Lessons(db.Model):
    __tablename__ = 'Lessons'
    Id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    LessonName = db.Column(db.Text(), nullable=False)


class MarksList(db.Model):
    __tablename__ = 'MarksList'
    Id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    PupilId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)
    TeacherId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)
    Mark = db.Column(db.Integer(), nullable=False)
    TeacherDesc = db.Column(db.Text())


class MissedLessons(db.Model):
    __tablename__ = 'MissedLessons'
    Id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    UserId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)
    SkippedLessonDateTime = db.Column(db.Text(), nullable=False)
    SkippedAllDay = db.Column(db.Integer())
    SkipReasonTypeId = db.Column(db.Integer(), nullable=False)
    ElderDesc = db.Column(db.Text())


class MissedLessonsReason(db.Model):
    __tablename__ = 'MissedLessonsReason'
    SkipReasonName = db.Column(db.Text(), nullable=False, primary_key=True)


class ScheduleList(db.Model):
    __tablename__ = 'ScheduleList'
    Id = db.Column(db.Integer(), nullable=False, primary_key=True)
    LessonId = db.Column(db.Integer(), ForeignKey('Lessons.Id'), nullable=False)
    GroupsId = db.Column(db.Integer(), ForeignKey('Groups.Id'), nullable=False)
    TeacherId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)
    LessonDateTime = db.Column(db.Text(), nullable=False)


@login_manager.user_loader
def load_user(UserId):
    return Users.query.get(UserId)


@app.route('/', methods=['POST', 'GET'])
def Login():
    try:
        logout_user()
    except:
        pass
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(UserLogin=login).first()

        if check_password_hash(user.UserPassword, password):
            login_user(user)
            next_page = request.args.get('next')
            try:
                return redirect(next_page)
            except:
                return redirect(url_for('Main'))

        if not check_password_hash(user.UserPassword, password):
            flash('Error in login procession', category='error')
    return render_template('authorization.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('Login'))


@app.route('/main')
@login_required
def Main():
    return render_template('index.html')


@app.route('/main/timetable')
@login_required
def Schedule():
    return render_template('timetable.html')


@app.route('/main/teachers')
@login_required
def Teachers():
    return 'Учителя'


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Станица не найдена :(')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('Login'))
    return response


if __name__ == '__main__':
    app.run(debug=True)
