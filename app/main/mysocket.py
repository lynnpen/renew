# coding: utf-8
import os
from flask.ext.socketio import emit, join_room, leave_room, close_room, rooms, disconnect
from flask.ext.login import current_user
from flask import request
from datetime import datetime
from .. import db
from ..models import User, ChatLog
from .. import socketio
from binascii import a2b_base64
import logging
from PIL import Image, ExifTags
from StringIO import StringIO
import functools
import redis


size = (128, 128)
userlist_ = []
userlist = set(userlist_)

FILEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/upload'
THUMBNAILDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/thumbnail'

r = redis.StrictRedis(host='127.0.0.1', password='', port=6379, db=0)

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
        if current_user.username == 'test2':
            r.rpush('receivewx', message['data'])
        chat = ChatLog(time=datetime.now().strftime("%m/%d %H:%M"), username=current_user.username, chatlog=message['data'])
        db.session.add(chat)
        db.session.commit()
        logging.debug(current_user.username + ": " + message['data'])

@socketio.on('imgmsg', namespace='/chat')
@authenticated_only
def imgmessage(imgmsg):
    if imgmsg['data']:
        room = 'honeymoon'
        img_data = imgmsg['data'].split(',', 1)[1]
        img_type = imgmsg['data'].split(';', 1)[0].split('/', 1)[1]
        binary_data = a2b_base64(img_data)
        image_file = StringIO(binary_data)
        filename = current_user.username + '_' + datetime.now().strftime("%Y%m%d-%H:%M:%S") + '.' + img_type
        im = Image.open(image_file)
        lwrat = float(im.size[0]) / float(im.size[1])
        if im.size[0] > 1024:
            l = 1024
            w = int(l / lwrat)
        elif im.size[1] > 768:
            w = 768
            l = int(w * lwrat)
        else:
            w = im.size[1]
            l = im.size[0]
        im.resize((l, w))

        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' : break 
        exif = dict(im._getexif().items())

        if exif[orientation] == 3: 
            im = im.rotate(180, expand=True)
        elif exif[orientation] == 6: 
            im = im.rotate(270, expand=True)
        elif exif[orientation] == 8: 
            im = im.rotate(90, expand=True)

        im.save(FILEDIR + '/' + filename, "JPEG")
        im.thumbnail(size)
        im.save(THUMBNAILDIR + '/' + filename, "JPEG")

        emit('newimg', {'data': '%s[%s]: %s' % ( current_user.username, datetime.now().strftime("%m/%d %H:%M"), imgmsg['data'])}, room=room)
        chat = ChatLog(time=datetime.now().strftime("%m/%d %H:%M"), username=current_user.username, chatlog='filename:' + filename)
        db.session.add(chat)
        db.session.commit()
        logging.debug(current_user.username + ": filename: " + filename)



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
        #emit('my response', {'data': '%s[%s] has Connected!' % (current_user.username, datetime.now().strftime("%m/%d %H:%M"))}, broadcast=True)
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
