import os
from app import create_app, db, socketio
from app.models import User, ChatLog
from flask.ext.socketio import SocketIO
import logging

logging.basicConfig(filename='message.log',level=logging.DEBUG, filemode = 'a+', format = '%(asctime)s - %(levelname)s: %(message)s')


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__ == '__main__':
    socketio.run(app)
