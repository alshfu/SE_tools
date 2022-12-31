import hashlib

import sqlalchemy
from sqlalchemy import func

from Model.Company import Companies
from Model.DB import db
from Model.DataBase.Accounting_account import References, Accounting_account
from Model.DataBase.TransactionsTable import TransactionsTable
from Model.DataBase.Verifications import Verifications as Verifications_from_db
from functions.functions import string_cleaner


class Account:
    def __init__(self, account_value):
        self.account = Accounting_account.query.filter_by(account=account_value).first()

    def get_account_id(self):
        return self.account.id


class Reference:
    def __init__(self, reference_str):
        self.reference_str = string_cleaner(reference_str.upper())

    def get_reference(self):
        print(self.reference_str)
        hash_of_reference = hashlib.sha256()
        hash_of_reference.update(self.reference_str.encode('utf-8'))
        hash_of_reference = hash_of_reference.hexdigest()
        print(hash_of_reference)
        # 60d8199d2aa6b992b4a78d37bc8e92e0d51918647b72873274db4e3fc0b70ce9
        print(References.query.filter_by(hash_of_reference=hash_of_reference).first())
        if References.query.filter_by(hash_of_reference=hash_of_reference).first() is None:
            try:
                reference = References(reference_str=self.reference_str)
                db.session.add(reference)
                db.session.flush()
                db.session.commit() # commit the changes to the database
                return reference
            except sqlalchemy.exc.IntegrityError:
                db.session.rollback()
                hash_of_reference = hashlib.sha256()
                hash_of_reference.update(string_cleaner(self.reference_str).encode('utf-8'))
                hash_of_reference = hash_of_reference.hexdigest()
                print(hash_of_reference)
                print('Reference already exists')
                return References.query.filter_by(hash_of_reference=hash_of_reference).first()
        else:
            return References.query.filter_by(hash_of_reference=hash_of_reference).first()



class Transactions:
    def __init__(self, verification_id, amount, reference, main_account=1930):
        self.reference = reference
        self.main_account_id = Account(account_value=main_account).get_account_id()
        self.amount = amount.replace(' ', '').replace(',', '.')
        self.verification_id = verification_id

    def create_transaction_for_main_account(self):
        transaction_from_db = TransactionsTable.query.filter_by(verification_id=self.verification_id,
                                                                amount=self.amount,
                                                                account_id=self.main_account_id).first()
        if transaction_from_db is None:
            transaction = TransactionsTable(verification_id=self.verification_id,
                                            id_from_file=1,
                                            amount=self.amount,
                                            account_id=self.main_account_id)
            db.session.add(transaction)
            db.session.flush()
            return transaction
        else:
            return transaction_from_db

    def create_transaction_for_secondary_account(self):
        if self.reference.account_id is None:
            transaction = TransactionsTable(verification_id=self.verification_id,
                                            amount=-1 * float(self.amount),
                                            id_from_file=2)
            db.session.add(transaction)
            db.session.flush()
            return transaction
        else:
            transaction = TransactionsTable(verification_id=self.verification_id,
                                            amount=-1 * float(self.amount),
                                            id_from_file=2,
                                            account_id=self.reference.account_id)
            db.session.add(transaction)
            db.session.flush()
            return transaction

    def create_new_transactions(self):
        self.create_transaction_for_main_account()
        self.create_transaction_for_secondary_account()


class Verification:
    def __init__(self, id_from_file, type_of_verifications, reference_id, company_id, period, date):
        self.id_from_file = id_from_file
        self.type_of_verifications = type_of_verifications
        self.reference_id = reference_id
        self.company_id = company_id
        self.period = period
        self.date = date

    def get_verification(self):
        verification_from_db = Verifications_from_db.query.filter_by(type_of_verifications=self.type_of_verifications,
                                                                     id_from_file=self.id_from_file,
                                                                     reference_id=self.reference_id,
                                                                     company_id=self.company_id,
                                                                     period=self.period,
                                                                     date=self.date).first()
        if verification_from_db is None:
            print("verifications is New")
            verification = Verifications_from_db(type_of_verifications=self.type_of_verifications,
                                                 id_from_file=self.id_from_file,
                                                 reference_id=self.reference_id,
                                                 company_id=self.company_id,
                                                 period=self.period,
                                                 date=self.date)
            db.session.add(verification)
            db.session.flush()
            return verification
        else:
            print("verifications is NOT new")
            return verification_from_db


class Verifications:
    def __init__(self, form_data):
        self.form_data = form_data
        self.company_id = self.get_company().id

    def get_company(self):
        company_name = (self.form_data.get('company_name'))
        company_bic = (self.form_data.get('bic'))
        period = f"""{self.form_data.getlist('date')[0]} / {self.form_data.getlist('date').pop()}"""
        company = Companies(name=company_name, bic=company_bic, period=period).get_company()
        return company

    def create_verification(self, index):
        id_from_file = self.form_data.getlist('id')[index]
        type_of_verifications = 'A'
        date = self.form_data.getlist('date')[index]
        reference_str = self.form_data.getlist('reference')[index]
        amount = self.form_data.getlist('amount')[index]
        reference = Reference(reference_str=reference_str).get_reference()
        period = f"""{self.form_data.getlist('date')[0]} / {self.form_data.getlist('date').pop()}"""

        verification = Verification(id_from_file=id_from_file,
                                    type_of_verifications=type_of_verifications,
                                    reference_id=reference.id,
                                    company_id=self.company_id,
                                    period=period,
                                    date=date).get_verification()
        Transactions(verification_id=verification.id,
                     amount=amount,
                     reference=reference).create_new_transactions()
        print(f"""verification id => {verification.id} id => {id_from_file} | date => {date} | ref-id {reference.id}| ref_str => {reference_str} | amount
         {amount}""")
        db.session.commit()

    def create_verifications_from_csv(self):
        count_of_verifications = len(self.form_data.getlist('id'))
        print(count_of_verifications)
        print(self.form_data)

        print(f"""company id is {self.company_id}""")
        for i in range(count_of_verifications):
            self.create_verification(index=i)
