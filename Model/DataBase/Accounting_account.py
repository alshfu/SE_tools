import hashlib

from flask_login import current_user
from sqlalchemy import Sequence

from Model.DB import db
from functions.functions import string_cleaner


class Accounting_account(db.Model):
    __tablename__ = "accounting_account"

    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    account = db.Column(db.Integer)
    description = db.Column(db.String())
    references = db.relationship('References', backref='accounting_account', lazy=True)
    vat = db.Column(db.Float)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, account=0, vat=0, description=''):
        self.user = current_user.id
        self.account = account
        self.vat = vat
        self.description = string_cleaner(description)


class References(db.Model):
    __tablename__ = "references"

    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    reference_str = db.Column(db.String(), nullable=False, unique=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounting_account.id'), nullable=True)
    hash_of_reference = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, reference_str='', account_id=None):
        hash_of_reference = hashlib.sha256()
        self.account_id = account_id
        self.reference_str = string_cleaner(reference_str.upper())
        hash_of_reference.update(reference_str.encode('utf-8'))
        self.hash_of_reference = hash_of_reference.hexdigest()
