from flask_restplus import reqparse

verify_email = reqparse.RequestParser()
verify_email.add_argument('auth_token',type=str,required=True,help='Authorization key')
verify_email.add_argument('activation_code',type=str,required=True,help='Activation code')
verify_email.add_argument('public_id',type=str,required=True,help='User public id')