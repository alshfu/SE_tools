from flask_login import current_user
from sqlalchemy import Sequence

from Model.DB import db



class Companies(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    bic = db.Column(db.Integer)
    name = db.Column(db.String(120))
    period = db.Column(db.String, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # transactions = db.relationship('TransactionsTable', backref='company', lazy=True)
    transactions  = db.relationship('TransactionsTable', lazy='select', backref=db.backref('company', lazy='joined'))

    def __init__(self, bic, name, period):
        self.user = current_user.id
        self.bic = bic
        self.name = name
        self.period = period
