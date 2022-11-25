from flask_login import current_user
from sqlalchemy import Sequence

from Model.DB import db



class Accounting_account(db.Model):
    __tablename__ = "accounting_account"
    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    account = db.Column(db.Integer)
    description = db.Column(db.String())
    references = db.relationship('References', backref='accounting_account', lazy=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, account = 0):
        self.user = current_user.id
        self.account = account


class References(db.Model):
    __tablename__ = "references"
    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    reference_str = db.Column(db.String())
    account_id = db.Column(db.Integer, db.ForeignKey('accounting_account.id'), nullable=True)
    transactions = db.relationship('TransactionsTable', backref='reference', lazy=True)

    def __init__(self, reference_str=None, account_id=None):
        self.account_id = account_id
        self.reference_str = reference_str
