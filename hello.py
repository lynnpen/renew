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
from wtforms.validators import Required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os, time, eventlet
import logging

async_mode = 'eventlet'


logging.basicConfig(filename='message.log',level=logging.DEBUG, filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s')
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'wocawoca'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
#manager = Manager(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

socketio = SocketIO(app, async_mode=async_mode)
thread = None

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
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



class LoginForm(Form):
    name = StringField('name', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember me', default = False)
    submit = SubmitField('Log In')

class ModPassword(Form):
    oldpassword = PasswordField('old password', validators=[Required()])
    newpassword = PasswordField('new password', validators=[Required()])
    new2password = PasswordField('repeat new password', validators=[Required()])
    submit = SubmitField('comfirm')

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
    name = current_user.username
    return render_template('index.html', name=name)


@app.route('/modpass', methods=['GET', 'POST'])
@login_required
def modpass():
    form = ModPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        new1 = form.newpassword.data
        new2 = form.new2password.data
        if user.verify_password(form.oldpassword.data) and new1 != '' and new2 != '':
            if new1 != new2:
                flash('please check your input')
            elif new1 == new2:
                user = User.query.filter_by(username=current_user.username).first()
                user.password = new1
                user.password_hash
                db.session.delete(user)
                db.session.add(user)
                db.session.commit()
                flash('modify password success!')
    return render_template('mod.html', form=form)

@app.route('/logout')
def logout():
    user = User.query.filter_by(username=current_user.username).first()
    login_user(user, True)
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

#@app.route('/test')
#def test():
#    return render_template('index.html')

@socketio.on('my event', namespace='/chat')
def message(message):
    if message['data']:
        emit('my response', {'data': '%s: %s' % (current_user.username, message['data'])}, broadcast=True)
        logging.debug(current_user.username + ": " + message['data'])

@socketio.on('connect', namespace='/chat')
def connect():
    if current_user.is_authenticated:
        emit('my response', {'data': '{0} has Connected!'.format(current_user.username)}, broadcast=True)
    else:
        return False


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    pass

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])
    print(request.event["args"])


if __name__ == '__main__':
    socketio.run(app)
    #socketio.run(app, host='0.0.0.0', port=80, debug=True)
