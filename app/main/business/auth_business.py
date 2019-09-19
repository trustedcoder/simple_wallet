import datetime
from app.main.model.user import User
from app.main import db
from app.main import config
from . import random_sample
from .. import encrypter


class Auth:
    @staticmethod
    def email_register(data):
        if data['auth_token'] == config.API_TOKEN_KEY:
            # Check if username already exist in database
            response1 = Auth.is_username_exist(data)
            if response1['status'] == 1:
                # username already exist, do not create account
                response_object = {
                    'status': 0,
                    'message': 'Username Already exist'
                }
                return response_object
            else:
                # check if email already exit
                response2 = Auth.is_email_exist(data)
                if response2['status'] == 1:
                    # email already exist, do not create account
                    response_object = {
                        'status': 0,
                        'message': 'Email Already exist'
                    }
                    return response_object
                else:
                    wallet_id = ('\n'.join(map(str, random_sample(1, 2, 1000000))))
                    tran_code = 'address_' + ('\n'.join(map(str, random_sample(1, 2, 100000000000000000000))))
                    pin = encrypter.encrypt(str(data['pin']))
                    agent_id = '0'
                    if data['account_type'] == 1:
                        # user is an agent
                        agent_id = ('\n'.join(map(str, random_sample(1, 2, 1000000000000))))
                    new_user = User(
                        email=data['email'],
                        wallet_id = wallet_id,
                        chain_address = tran_code,
                        pin = pin,
                        account_type = data['account_type'],
                        agent_id = agent_id,
                        username=data['username'],
                        password=User.generate_password(data['password']),
                        access=1,
                        date_created=datetime.datetime.utcnow()
                    )
                    Auth.save_changes(new_user)

                    # call the below method to login the user immediately.
                    data_login = {
                        'auth_token': data['auth_token'],
                        'email': data['email'],
                        'password': data['password']
                    }
                    return Auth.email_login(data_login)
        else:
            response_object = {
                'status': 0,
                'message': 'Not recognized'
            }
            return response_object

    @staticmethod
    def email_login(data):
        if data['auth_token'] == config.API_TOKEN_KEY:
            try:
                # fetch the user data
                user = User.query.filter(User.email==data['email']).first()
                if user and User.check_password(user.password,data['password']):
                    if user.access == config.ACTIVE_USER:
                        response1 = user.encode_auth_token(user.id)
                        if response1['status'] == 1:
                            if user.account_type == 1:
                                # for the agent
                                response_object = {
                                    'status': 1,
                                    'wallet_id':user.wallet_id,
                                    'agent_id': user.agent_id,
                                    'message': 'Successfully logged in.',
                                    'authorization': response1['token'].decode()
                                }
                                return response_object
                            else:
                                # for other users
                                response_object = {
                                    'status': 1,
                                    'wallet_id': user.wallet_id,
                                    'message': 'Successfully logged in.',
                                    'authorization': response1['token'].decode()
                                }
                                return response_object
                        else:
                            response_object = {
                                'status': 0,
                                'message': response1['message']
                            }
                            return response_object
                    else:
                        response_object = {
                            'status': 0,
                            'message': 'Your account is disabled.'
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'Invalid Details.'
                    }
                    return response_object

            except Exception as e:
                print(e)
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try again'
                }
                return response_object

        else:
            response_object = {
                'status': 10,
                'message': 'Blocked',
            }
            return response_object


    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                user = User.query.filter_by(id=resp['user_id']).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'registered_on': str(user.date_created)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 0,
                'message': resp['message']
            }
            return response_object, 401
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object, 401

    @staticmethod
    def is_username_exist(data):
        found = User.query.filter_by(username=data['username']).first()
        if found:
            response_object = {
                'status': 1,
                'message': 'Username already exists.',
            }
            return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Username not found.',
            }
            return response_object

    @staticmethod
    def is_email_exist(data):
        found = User.query.filter_by(email=data['email']).first()
        if found:
            response_object = {
                'status': 1,
                'message': 'Email already exists.',
            }
            return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Email not found.',
            }
            return response_object

    @staticmethod
    def save_changes(data):
        db.session.add(data)
        db.session.commit()