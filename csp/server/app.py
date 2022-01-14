import calendar
import os
from flask import Flask, render_template, request, redirect, url_for, g, abort, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, login_user, login_required, UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from jinja2 import environment


def out_none(val):
    for t in val:
        if not t is None or t != 'None' or t != '' or t != 'none':
            t = t
        else:
            t = ''
    return val


environment.DEFAULT_FILTERS['out_none'] = out_none

# session.modified = True
cur_id = int
period = str

empty_marks = {
    "Математика": [],
    "Физика": [],
    "Астрономия": [],
    "Физкультура": [],
    "Информатика": [],
    "Английский Язык": [],
    "Русский Язык": [],
    "История": [],
    "Обществознание": [],
    "Биология": [],
    "Литература": [],
    "Обж": []
}
# !config info!
SECRET_KEY = 'so-so-so-so-so-difficult-key'
DATABASE = '/csp/server/nkedb.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nkedb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'nkedb.db')))
app.config['SECRET_KEY'] = '3e301b1682e2833089377a8c440e19416ac7f6c9'
app.permanent_session_lifetime = datetime.timedelta(days=7)

db = SQLAlchemy(app)

login_manager = LoginManager(app)


def get_lessons(*name):
    list_of_lessons = []
    for i in name:
        lesson = Lessons.query.filter_by(LessonName=i).first()
        list_of_lessons.append(lesson)
        print(list_of_lessons, lesson)
    return list_of_lessons


def get_marks(id):
    marks = []
    iter = 0
    while True:
        iter += 1
        try:
            mark = MarksList.query.filter_by(Id=iter).first()
            if mark.PupilId == id:
                l = Lessons.query.filter_by(Id=mark.LessonId).first()
                marks.append(l.LessonName)
                marks.append(mark.Mark)
        except:
            break
    try:
        dict = {marks[i]: marks[i + 1] for i in range(0, len(marks), 2)}
        return dict
    except:
        return {}


def get_schedule(cur_day):
    pairs = []
    iter = 0
    l = ScheduleList.query.filter_by(LessonDate=cur_day).all()
    while True:
        try:
            iter += 1
            temp = ScheduleList.query.filter_by(Id=iter).first()
            if temp.LessonDate == cur_day:
                pairs.append(temp)
        except:
            break
    return pairs


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
        return '<UserId %r>' % self.UserId


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
    Id = db.Column(db.Integer, nullable=False, unique=True)
    LessonName = db.Column(db.Text(), nullable=False, primary_key=True)

    def __repr__(self):
        return 'LessonId %r>' % (self.Id)


class MarksList(db.Model):
    __tablename__ = 'MarksList'
    Id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    PupilId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)
    LessonId = db.Column(db.Integer(), ForeignKey('Lessons.Id'), nullable=False)
    Mark = db.Column(db.Integer(), nullable=False)
    TeacherDesc = db.Column(db.Text())
    Date = db.Column(db.Text())

    def __repr__(self):
        return str(self.Mark)


class MissedLessons(db.Model):
    __tablename__ = 'MissedLessons'
    Id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    UserId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)
    SkippedLessonDate = db.Column(db.Text(), nullable=False)
    IsSkippedAllLesson = db.Column(db.Integer())
    SkipReasonTypeId = db.Column(db.Integer(), nullable=False)
    ElderDesc = db.Column(db.Text())
    SkippedLessonTime = db.Column(db.Text())
    SkippedLessonId = db.Column(db.Integer(), ForeignKey('Lessons.Id'))


class MissedLessonsReason(db.Model):
    __tablename__ = 'MissedLessonsReason'
    SkipReasonName = db.Column(db.Text(), nullable=False, primary_key=True)


class ScheduleList(db.Model):
    __tablename__ = 'ScheduleList'
    Id = db.Column(db.Integer(), nullable=False, primary_key=True)
    GroupId = db.Column(db.Integer(), ForeignKey('Groups.Id'), nullable=False)
    TeacherId = db.Column(db.Integer(), ForeignKey('Users.UserId'), nullable=False)
    LessonTime = db.Column(db.Text())
    LessonDate = db.Column(db.Text())
    LessonId = db.Column(db.Integer(), ForeignKey('Lessons.LessonId'), nullable=False)
    Office = db.Column(db.Text(), ForeignKey('Offices.Audience'))

    def __repr__(self):
        return self.LessonDate


def filter_suppress_none(val):
    if not val is None:
        return val
    else:
        return ''


class Offices(db.Model):
    Audience = db.Column(db.Text(), primary_key=True, nullable=False)


@login_manager.user_loader
def load_user(UserId):
    return Users.query.get(UserId)


@app.route('/', methods=['POST', 'GET'])
def Login():
    session.permanent = True
    global cur_id
    if 'users_cookies' in session:
        cur_id = session['Users_id']
        return redirect(url_for('Main'), )
    else:
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
                cur_id = user.UserId
                login_user(user)
                next_page = request.args.get('next')
                try:
                    return redirect(next_page)
                except:
                    session['users_cookies'] = 1
                    session['Users_id'] = cur_id
                    return redirect(url_for('Main'), )

            if not check_password_hash(user.UserPassword, password):
                flash('Error in login procession', category='error')
                return render_template('authorization.html')
    return render_template('authorization.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        session['Users_id'] = None
    except:
        return redirect(url_for('Login'))
    return redirect(url_for('Login'))


@app.route('/main', methods=['POST', 'GET'])
@login_required
def Main():
    global cur_id
    global period
    user = load_user(cur_id)

    day = str(datetime.date.today().day)
    month = str(datetime.date.today().month)
    if len(month) != 2:
        month = '0' + month
    period = day + "." + month
    schedules = get_schedule(period)

    cur_day = datetime.datetime.today().isoweekday()
    cur_day -= 1
    allMarks = db.session.query(MarksList).filter(MarksList.Date.between /
                ((int(day) - cur_day), (int(day) - cur_day) + 7)).filter(MarksList.PupilId == cur_id).all()

    for i in empty_marks.keys():
        for j in allMarks:
            if i == (Lessons.query.filter_by(Id=j.LessonId).first()).LessonName:
                empty_marks[i].append(j)

    return render_template('main.html',
                           allMarks=allMarks,
                           empty_marks=empty_marks,
                           Lessons=Lessons,
                           period=period,
                           schedules=schedules,
                           )


@app.route('/timetable')
@login_required
def Schedule():
    global cur_id
    day = str(datetime.date.today().day)
    month = str(datetime.date.today().month)
    if len(month) != 2:
        month = '0' + month
    period = day + "." + month
    cur_day = datetime.datetime.today().isoweekday()
    cur_day -= 1

    lessons = ScheduleList.query.filter(ScheduleList.LessonDate.between /
                ((int(day) - cur_day), (int(day) - cur_day) + 7)).all()
    dates = []
    for i in lessons:
        dates.append(i.LessonDate)
    dates = list(set(dates))
    dates = sorted(dates)

    return render_template('schedule.html',
                           ScheduleList=ScheduleList,
                           cur_day=cur_day,
                           DAY=day,
                           int=int,
                           str=str,
                           Lessons=Lessons,
                           dates=dates,
                           datetime=datetime,
                           calendar=calendar,
                           )

@app.route('/teachers')
@login_required
def Teachers():
    return render_template('teachers.html')


@app.route('/journal')
@login_required
def Journal():
    Marks = []
    return render_template('journal.html',
                           user_id=str(cur_id),
                           items=13,
                           Lessons=Lessons,
                           MarksList=MarksList,
                           MissedLessons=MissedLessons,
                           int=int,
                           str=str,
                           len=len,
                           sum=sum,
                           )


@app.route('/forgotpass')
def Forgotpass():
    return render_template('forgotpass.html')


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
