from flask import request
from flask_restplus import Resource
from app.main.business.auth_business import Auth
from ..util.dto import AuthDto

api = AuthDto.api
email_register = AuthDto.email_register
email_login = AuthDto.email_login


@api.route('/email_register')
class EmailUserRegister(Resource):
   @api.expect(email_register)
   def post(self):
       """Register a new user or agent"""
       data = request.json
       return Auth.email_register(data)


@api.route('/email_login')
class EmailUserLogin(Resource):
    @api.expect(email_login)
    def post(self):
        """Login user or agent"""
        data = request.json
        return Auth.email_login(data)