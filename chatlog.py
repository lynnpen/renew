# coding: utf-8
import os
from app import create_app, db, socketio
from app.models import User, ChatLog
from flask.ext.socketio import SocketIO, emit
import logging
import redis
import time
from datetime import datetime
import threading

logging.basicConfig(filename='message.log',level=logging.DEBUG, filemode = 'a+', format = '%(asctime)s - %(levelname)s: %(message)s')

r = redis.StrictRedis(host='127.0.0.1', password='', port=6379, db=0)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

def check_wx():
    with app.app_context():
        while True:
            text = r.lpop('sendwx')
            #r.delete('sendwx')
            if text:
                text = text.decode('utf-8')
                emit('my response', {'data': 'test1[%s]: %s' % (datetime.now().strftime("%m/%d %H:%M"), text)}, room='honeymoon', namespace='/chat')
                chat = ChatLog(time=datetime.now().strftime("%m/%d %H:%M"), username='test1', chatlog=text)
                db.session.add(chat)
                db.session.commit()
                logging.debug( "test1: " + text)
            time.sleep(1)


if __name__ == '__main__':
    t = threading.Thread(target=check_wx, args=())
    t.setDaemon(True)
    t.start()

    socketio.run(app)

