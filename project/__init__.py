from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import psycopg2
#import psycopg2.extras

db = SQLAlchemy()

def create_app():
    application = Flask(__name__)
    app = application

    app.config['SECRET_KEY'] = 'controle123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:controle123@dbcontrolechamados.cb4akgeqo179.us-east-1.rds.amazonaws.com:5432/db-controle-chamados'
    
    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


