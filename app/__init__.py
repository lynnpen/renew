import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.socketio import SocketIO
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
socketio = SocketIO()

async_mode = 'eventlet'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, message_queue='redis://', async_mode=async_mode)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
