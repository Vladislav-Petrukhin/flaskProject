from flask_pymongo import PyMongo
from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from flask_session import Session
from config import Config

mongo = PyMongo()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)

    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


mongo = PyMongo()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)

    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
