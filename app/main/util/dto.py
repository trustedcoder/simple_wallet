from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='authentication related operations')

    email_register = api.model('email_register',{
        'auth_token': fields.String(required=True, description='Authorization key'),
        'username': fields.String(required=True, description='Username of the user', max_length=14, min_length=4,pattern='(^[a-zA-Z0-9][a-zA-Z0-9_]*$)'),
        'email': fields.String(required=True, description='Email of the user',pattern='(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
        'password': fields.String(required=True, description='Password of the user', min_length=6),
        'pin': fields.Integer(required=True, description='PIN used for transaction', min_length=4,max_length=4),
        'account_type': fields.Integer(required=True, description='Account Type. 1 is agent and 0 is other users', pattern='(^[0-1][0-1_]*$)',max_length=1),
    })

    email_login = api.model('email_login', {
        'auth_token': fields.String(required=True, description='Authorization key'),
        'email': fields.String(required=True, description='Email of the user'),
        'password': fields.String(required=True, description='Password of the user', min_length=6)
    })


class TranDto:
    api = Namespace('transaction', description='Transaction related operations')
    move_fund = api.model('move_fund', {
        'amount': fields.Integer(required=True, description='Amount to be sent'),
        'wallet_id': fields.String(required=True, description='Wallet ID of the receiving user'),
        'pin': fields.Integer(required=True, description='Agent PIN'),
        'otp': fields.Integer(required=True, description='OTP sent to phone (Since this is a test, You can generate one here.)'),
    })
    fund_agent = api.model('fund_agent', {
        'amount': fields.Integer(required=True, description='Amount to be sent'),
        'wallet_id': fields.String(required=True, description='Wallet ID of the receiving agent'),
        'admin': fields.String(required=True, description='Just for a test (trustedcoder)'),
    })