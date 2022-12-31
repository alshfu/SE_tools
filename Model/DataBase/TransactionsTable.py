from flask_login import current_user
from sqlalchemy import Sequence

from Model.DB import db


class TransactionsTable(db.Model):
    __tablename__ = "transactions"

    verification_id = db.Column(db.Integer, db.ForeignKey('verifications.id'), nullable=True)
    # id
    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    # id from file
    id_from_file = db.Column(db.Integer, nullable=True)
    # owner
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # amount
    amount = db.Column(db.Float)
    # reference
    comment = db.Column(db.String)
    # file
    file = db.Column(db.String)
    # account
    account_id = db.Column(db.Integer, db.ForeignKey('accounting_account.id'), nullable=True)
    account = db.relationship('Accounting_account', lazy='select', backref=db.backref('transaction', lazy='joined'))

    # vat
    vat = db.Column(db.Float)

    def __init__(self,
                 verification_id=None,
                 id_from_file=None,
                 amount=None,
                 account_id=None,
                 reference_id=0,
                 comment=None,
                 file=None,
                 vat=0,
                 ):
        self.verification_id = int(verification_id)
        self.id_from_file = int(id_from_file)
        self.user_id = current_user.id
        self.amount = float(amount)
        self.reference_id = int(reference_id)
        self.comment = comment
        self.file = file
        self.vat = float(vat)
        if account_id is None:
            self.account_id = None
        else:
            self.account_id = int(account_id)
