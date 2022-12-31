from flask_login import current_user
from sqlalchemy import Sequence
from Model.DataBase.Company import Companies

from Model.DB import db


class Verifications(db.Model):
    __tablename__ = "verifications"

    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)

    type_of_verifications = db.Column(db.String(1))
    id_from_file = db.Column(db.Integer)
    reference_id = db.Column(db.Integer, db.ForeignKey('references.id'), nullable=True)
    transactions = db.relationship('TransactionsTable', lazy='select', backref=db.backref('verification', lazy='joined'))
    reference = db.relationship('References', lazy='select', backref=db.backref('verification', lazy='joined'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    period = db.Column(db.String, nullable=False)
    file = db.Column(db.String)
    date = db.Column(db.String)
    comment = db.Column(db.String)

    def __init__(self,
                 file = None,
                 type_of_verifications = 'A',
                 id_from_file = None,
                 reference_id = None,
                 company_id = None,
                 period = None,
                 date = None):
        self.file = file
        self.type_of_verifications = type_of_verifications
        self.id_from_file = id_from_file
        self.reference_id = reference_id
        self.user_id = current_user.id
        self.company_id = company_id
        self.date = date
        self.period = period
