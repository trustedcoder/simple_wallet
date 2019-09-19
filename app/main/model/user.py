from .. import db,flask_bcrypt
import datetime
import jwt
from ..config import key


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True,nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    wallet_id = db.Column(db.String(255), unique=True, nullable=False)
    chain_address = db.Column(db.String(255), unique=True, nullable=False)
    pin = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.Integer, nullable=False)
    agent_id = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255))
    access = db.Column(db.Integer, default=1, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)


    @staticmethod
    def generate_password(pass_word):
        return flask_bcrypt.generate_password_hash(pass_word).decode('utf-8')

    @staticmethod
    def check_password(password,pass_word):
        return flask_bcrypt.check_password_hash(password, pass_word)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=200, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            auth_token = jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
            response_object = {
                'status': 1,
                'message': 'Authorization Token generated successfully',
                'token': auth_token,
            }
            return response_object
        except Exception as e:
            response_object = {
                'status': 0,
                'message': 'An error occurred. Try Again',
            }
            return response_object

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        """
        try:
            payload = jwt.decode(auth_token, key)
            response_object = {
                'status': 1,
                'message': 'Authorization Token Decoded successfully',
                'user_id': payload['sub'],
                'expire_date': payload['exp'],
            }
            return response_object
        except jwt.ExpiredSignatureError:
            response_object = {
                'status': 0,
                'message': 'Blocked.',
            }
            return response_object
        except jwt.InvalidTokenError:
            response_object = {
                'status': 0,
                'message': 'Blocked.',
            }
            return response_object