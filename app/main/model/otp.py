from .. import db
import datetime


class OTP(db.Model):

    __tablename__ = 'otp'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,nullable=False)
    otp = db.Column(db.String(225), unique=True, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, otp,user_id,expire_date):
        self.otp = otp
        self.user_id = user_id
        self.expire_date = expire_date
        self.date_created = datetime.datetime.now()

    def __repr__(self):
        return '<id: otp: {}'.format(self.otp)