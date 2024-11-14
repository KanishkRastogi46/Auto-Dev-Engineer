from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv


load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    from app.models.user import User
    with app.app_context():
        db.create_all()

    from app.routes.user import user
    from app.routes.chat import chat
    app.register_blueprint(user , url_prefix="/users")
    app.register_blueprint(chat , url_prefix="/chat")

    return app