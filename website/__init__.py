from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import subprocess as terminal_command

db = SQLAlchemy()
DB_NAME = "gameservernew.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Batman12"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix = '/')

    from . import Models

    with app.app_context():
        db.create_all()
        print('Created Database!')


    return app