from flask_restplus import Resource
from app.main.util.decorator import token_required
from flask import request
from app.main.business.tran_business import TranFuntion
# from ..util.req_parser import object_upload,get_apk,delete_apk
from ..util.dto import TranDto
api = TranDto.api
move_fund = TranDto.move_fund
fund_agent = TranDto.fund_agent


@api.route('/move_fund')
class MoveFund(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    @api.expect(move_fund)
    def post(self):
        """Used by agent to move fund to a wallet ID"""
        auth_header = request.headers.get('authorization')
        data = request.json
        return TranFuntion.moveFund(auth_token=auth_header,data=data)

@api.route('/generate_otp')
class GenerateOTP(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    def post(self):
        """For test purpose. Used for generating OTP"""
        auth_header = request.headers.get('authorization')
        return TranFuntion.generateOTP(auth_token=auth_header)

@api.route('/fund_an_agent')
class FundAgent(Resource):
    @api.expect(fund_agent)
    def post(self):
        """For test purpose. Used when an agent wants to fund their account"""
        data = request.json
        return TranFuntion.fundAnAgent(data)


@api.route('/get_history')
class TransactionHistory(Resource):
    @token_required
    @api.header('authorization', 'JWT TOKEN')
    def get(self):
        """Get all the transaction history of any user"""
        auth_header = request.headers.get('authorization')
        return TranFuntion.transaction_history(auth_token=auth_header)
