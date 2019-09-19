from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import config_by_name
from app.main.business.EnCryto import EnCryto
from app.main.business.ajocard_blockchain import AjoCardChain

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
ajocardchain = AjoCardChain()
encrypter = EnCryto('2345678kjhgfhjhgvg$#$%^IUKJGVBHJGFXSTE%RTUGJXFGCJHGHRDTYTGUJHVCHGDYRTTREWdsfdfgbkjvh')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app