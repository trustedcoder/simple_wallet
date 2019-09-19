from app.main.model.user import User
from app.main.model.otp import OTP
from app.main import db
from app.main import ajocardchain
from datetime import datetime,timedelta
from .. import encrypter
from . import random_sample


class TranFuntion:
    @staticmethod
    def moveFund(auth_token, data):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_agent = User.query.filter(User.id == resp['user_id']).first()
                if found_agent:
                    if found_agent.account_type == 1:
                        # check that OTP is valid
                        is_otp_valid = TranFuntion.is_otp_valid(data['otp'],resp['user_id'])
                        if is_otp_valid:
                            # check that Agent PIN is valid
                            is_agent_pin_valid = TranFuntion.is_pin_valid(data['pin'],resp['user_id'])
                            if is_agent_pin_valid:
                                # check that the wallet ID belongs to a user
                                wallet_response = TranFuntion.get_address_by_wallet_id(data['wallet_id'])
                                if wallet_response['status'] == 1:
                                    # check blockchain to ensure it has not been altered
                                    is_valid_chain = ajocardchain.valid_chain()
                                    if is_valid_chain:
                                        # check if the transaction to be performed is valid
                                        is_transaction_valid = ajocardchain.valid_transaction(found_agent.chain_address,int(data['amount']))
                                        if is_transaction_valid:
                                            # Move fund here
                                            tran_date = datetime.utcnow()
                                            result = ajocardchain.new_block(found_agent.chain_address,wallet_response['address'],int(data['amount']),1,1,tran_date,tran_date)
                                            if result:
                                                response_object = {
                                                    'status': 1,
                                                    'message': 'Fund successfully sent.'
                                                }
                                                return response_object
                                            else:
                                                response_object = {
                                                    'status': 0,
                                                    'message': 'Unknown error occurred. Please try again later'
                                                }
                                                return response_object
                                        else:
                                            response_object = {
                                                'status': 0,
                                                'message': 'Insufficient fund.'
                                            }
                                            return response_object
                                    else:
                                        response_object = {
                                            'status': 0,
                                            'message': 'System error. Please contact support.'
                                        }
                                        return response_object
                                else:
                                    response_object = {
                                        'status': 0,
                                        'message': 'Wallet ID is not valid. Kindly check your input.'
                                    }
                                    return response_object
                            else:
                                response_object = {
                                    'status': 0,
                                    'message': 'Invalid PIN.'
                                }
                                return response_object
                        else:
                            response_object = {
                                'status': 0,
                                'message': 'OTP invalid or expired.'
                            }
                            return response_object
                    else:
                        response_object = {
                            'status': 0,
                            'message': 'You are not an agent.'
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'User not found.'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def generateOTP(auth_token):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_agent = User.query.filter(User.id == resp['user_id']).first()
                if found_agent:
                    if found_agent.account_type == 1:
                        # check that OTP is valid
                        otp = ('\n'.join(map(str, random_sample(1, 2, 1000000))))
                        expire_date = datetime.utcnow() + timedelta(minutes=5)
                        new_otp = OTP(
                            otp=otp,
                            user_id = resp['user_id'],
                            expire_date = expire_date
                        )
                        db.session.add(new_otp)
                        db.session.commit()
                        response_object = {
                            'status': 1,
                            'otp':otp,
                            'message': 'OTP generated and will expire in 5 minutes.'
                        }
                        return response_object
                    else:
                        response_object = {
                            'status': 0,
                            'message': 'You are not an agent.'
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'User not found.'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def fundAnAgent(data):
        if data['admin'] == 'trustedcoder':
            found_agent = User.query.filter(User.wallet_id == data['wallet_id']).first()
            if found_agent:
                if found_agent.account_type == 1:
                    # check that the wallet ID belongs to a user
                    wallet_response = TranFuntion.get_address_by_wallet_id(data['wallet_id'])
                    if wallet_response['status'] == 1:
                        # check blockchain to ensure it has not been altered
                        is_valid_chain = ajocardchain.valid_chain()
                        if is_valid_chain:
                            # check if the transaction to be performed is valid
                            is_transaction_valid = ajocardchain.valid_transaction('ajocard_admin2',int(data['amount']))
                            if is_transaction_valid:
                                # Move fund here
                                tran_date = datetime.utcnow()
                                result = ajocardchain.new_block('ajocard_admin2', wallet_response['address'],int(data['amount']), 2, 2, tran_date, tran_date)
                                if result:
                                    response_object = {
                                        'status': 1,
                                        'message': 'Fund successfully sent.'
                                    }
                                    return response_object
                                else:
                                    response_object = {
                                        'status': 0,
                                        'message': 'Unknown error occurred. Please try again later'
                                    }
                                    return response_object
                            else:
                                response_object = {
                                    'status': 0,
                                    'message': 'Insufficient fund.'
                                }
                                return response_object
                        else:
                            response_object = {
                                'status': 0,
                                'message': 'System error. Please contact support.'
                            }
                            return response_object
                    else:
                        response_object = {
                            'status': 0,
                            'message': 'Wallet ID is not valid. Kindly check your input.'
                        }
                        return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'You are not an agent.'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'User not found.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def transaction_history(auth_token):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if resp['status'] == 1:
                found_user = User.query.filter(User.id == resp['user_id']).first()
                if found_user:
                    history_list = ajocardchain.transaction_history(found_user.chain_address)
                    store_list = []
                    for history in history_list:
                        if history['partner'] == 'ajocard_admin2':
                            the_other = 'ADMIN'
                        else:
                            resp_user = User.query.filter(User.chain_address == history['partner']).first()
                            the_other = resp_user.username
                        store_list.append({
                            'is_credited': history['is_credited'],
                            'amount': history['amount'],
                            'from_or_to': the_other,
                            'date': str(history['date'])
                        })
                    response_object = {
                        'status': 1,
                        'history': store_list,
                        'message': 'Transaction history fetched successfully'
                    }
                    return response_object
                else:
                    response_object = {
                        'status': 0,
                        'message': 'User not found.'
                    }
                    return response_object
            else:
                response_object = {
                    'status': 0,
                    'message': 'An error occurred. Try Again.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Blocked.'
            }
            return response_object

    @staticmethod
    def is_otp_valid(otp,user_id):
        found = OTP.query.filter(OTP.otp==otp,OTP.user_id == user_id).first()
        if found:
            # check if OTP is expired
            date_now = datetime.utcnow()
            duration = found.expire_date - date_now
            duration_in_s = duration.total_seconds()
            if duration_in_s > 0:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def is_pin_valid(pin, user_id):
        found = User.query.filter(User.id == user_id).first()
        if found:
            # decrypt the pin
            str_pin = encrypter.decrypt(found.pin)
            if str(str_pin) == str(pin):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def get_address_by_wallet_id(wallet_id):
        found = User.query.filter(User.wallet_id == wallet_id).first()
        if found:
            response_object = {
                'status': 1,
                'address': found.chain_address,
                'message': 'Invalid wallet ID'
            }
            return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Invalid wallet ID'
            }
            return response_object

    @staticmethod
    def save_changes(data):
        db.session.add(data)
        db.session.commit()