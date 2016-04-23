from flask.ext.socketio import emit, join_room, leave_room, close_room, rooms, disconnect
from flask.ext.login import current_user
from flask import request
from datetime import datetime
from .. import db
from ..models import User, ChatLog
from .. import socketio
import logging
import functools

userlist_ = []
userlist = set(userlist_)

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
        print userlist
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
