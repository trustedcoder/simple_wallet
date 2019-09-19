from flask_restplus import Api
from flask import Blueprint
from .main.endpoints.tran_endpoint import api as tran_ns
from .main.endpoints.auth_endpoint import api as auth_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='AjoCard Api',
          version='1.0',
          description='P2P Payment System ( Job Test)'
          )

api.add_namespace(auth_ns)
api.add_namespace(tran_ns)