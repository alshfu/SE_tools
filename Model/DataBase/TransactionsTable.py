from sqlalchemy import Sequence

from Model.DB import db


class TransactionsTable(db.Model):
    __tablename__ = "transactions"

    # id
    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    # id from file
    id_from_file = db.Column(db.Integer, nullable=True)
    # yyyy-mm-dd
    date = db.Column(db.String(10), nullable=False)
    # owner
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # company
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    # amount
    amount = db.Column(db.Float)
    # reference
    reference_id = db.Column(db.Integer, db.ForeignKey('references.id'), nullable=True)
   # reference = db.relationship('references', lazy='select', backref=db.backref('reference', lazy='joined'))
    # comment
    comment = db.Column(db.String)
    # file
    file = db.Column(db.String)
    # account
    account_id = db.Column(db.Integer, db.ForeignKey('accounting_account.id'), nullable=True)
    # period från / till åååå-mm-dd / åååå-mm-dd
    period = db.Column(db.String(24))
    # vat
    vat = db.Column(db.Float)

    def __init__(self,
                 id_from_file=None,
                 date=None,
                 user=None,
                 company_id=None,
                 amount=None,
                 reference_id=None,
                 comment=None,
                 file=None,
                 account=None,
                 vat=0,
                 period=None):
        self.id_from_file = id_from_file
        self.date = date
        self.user = user
        self.company_id = company_id
        self.amount = amount
        self.reference_id = reference_id
        self.comment = comment
        self.file = file
        self.account = account
        self.vat = vat
        self.period = period
