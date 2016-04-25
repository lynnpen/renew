from . import db
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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

