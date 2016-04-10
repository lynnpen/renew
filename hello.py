import eventlet
eventlet.monkey_patch()
from flask import Flask, request, redirect, render_template, url_for, session, flash, g
#from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import login_user, logout_user, UserMixin, LoginManager, login_required, current_user
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
#from threading import Thread
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Required, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import functools
import os, time, eventlet
import logging

async_mode = 'eventlet'
userlist_ = []
userlist = set(userlist_)


logging.basicConfig(filename='message.log',level=logging.DEBUG, filemode = 'a+', format = '%(asctime)s - %(levelname)s: %(message)s')
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'wocawoca'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/data.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
#manager = Manager(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

socketio = SocketIO(app, message_queue='redis://', async_mode=async_mode)
thread = None

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    userroom = db.Column(db.String(128))
#    sid = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
  
    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attibute')


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def is_authenticated(self):
        return True

class ChatLog(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(64))
    username = db.Column(db.String(64))
    chatlog = db.Column(db.String(256))


class LoginForm(Form):
    name = StringField('name', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember me', default = False)
    submit = SubmitField('Log In')

class ModPassword(Form):
    oldpassword = PasswordField('old password', validators=[Required()])
    newpassword = PasswordField('new password', validators=[Required(), EqualTo('new2password', message='Passwords must match')])
    new2password = PasswordField('repeat new password', validators=[Required()])
    submit = SubmitField('comfirm')

def check_user(user):
    rightone = User.query.filter_by(username=user).first()
    return rightone.userroom

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped  

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/modpass', methods=['GET', 'POST'])
@login_required
def modpass():
    form = ModPassword()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
                current_user.password = form.newpassword.data
                current_user.password_hash
                db.session.commit()
                flash('modify password success!')
    return render_template('mod.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@socketio.on('my event', namespace='/chat')
@authenticated_only
def message(message):
    if message['data']:
        room = 'honeymoon'
        emit('my response', {'data': '%s[%s]: %s' % ( current_user.username, datetime.now().strftime("%m/%d %H:%M"), message['data'])}, room=room)
        chat = ChatLog(time=datetime.now().strftime("%m/%d %H:%M"), username=current_user.username, chatlog=message['data'])
        db.session.add(chat)
        db.session.commit()
        logging.debug(current_user.username + ": " + message['data'])

@socketio.on('imgmsg', namespace='/chat')
@authenticated_only
def imgmessage(imgmsg):
    if imgmsg['data']:
        room = 'honeymoon'
        emit('newimg', {'data': '%s[%s]: %s' % ( current_user.username, datetime.now().strftime("%m/%d %H:%M"), imgmsg['data'])}, room=room)
        #chat = ChatLog(time=datetime.now().strftime("%m/%d %H:%M"), username=current_user.username, chatlog=imgmsg['data'])
        #db.session.add(chat)
        #db.session.commit()
        #logging.debug(current_user.username + ": " + imgmsg['data'])



@socketio.on('connect', namespace='/chat')
def connect():
    if current_user.is_authenticated and check_user(current_user.username):
        userlist.add(current_user.username)
        room = 'honeymoon'
        join_room(room) 
        chat = ChatLog()
        num = chat.query.count()
        n = 10
        while n>=0:
            msg = chat.query.get(num-n)
            emit('my response', {'data': '%s[%s]: %s' % (msg.username, msg.time, msg.chatlog) }, room=room)
            n -= 1
        emit('my response', {'data': '%s[%s] has Connected!' % (current_user.username, datetime.now().strftime("%m/%d %H:%M"))}, broadcast=True)
        emit('login', {'data': ' | '.join(userlist)}, broadcast=True)
    else:
        return False

@socketio.on('disconnect', namespace='/chat')
def disconnect():
    userlist.remove(current_user.username)
    emit('login', {'data': '|'.join(userlist)}, broadcast=True)

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])
    print(request.event["args"])


if __name__ == '__main__':
    socketio.run(app)
    #socketio.run(app, host='0.0.0.0', port=80, debug=True)
