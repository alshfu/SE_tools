import os

from flask_login import current_user
from werkzeug.utils import secure_filename

from Model.Company import Companies
from Model.DB import db
from Model.DataBase.Accounting_account import References, Accounting_account
from Model.DataBase.TransactionsTable import TransactionsTable
from config import UPLOAD_FOLDER_FOR_TRANSACTIONS_FILES
from functions.functions import create_uniq_file_name, remove_transaction_file, string_cleaner


class Transaction_from_se_file:

    def get_transaction(self) -> object:
        if self.get_check_if_transaction_exists():
            #print(self.transaction)
            return self.save_transaction()
        else:
            #print(self.transaction)
            return self.transaction

    def get_check_if_transaction_exists(self):
        if self.transaction is None:
            return True
        else:
            return False

    def save_transaction(self):
        if self.get_check_if_transaction_exists() is True:
            transaction = TransactionsTable(verification_id=self.verification_id[0],
                                                                 amount=self.amount[0],
                                                                 id_from_file=self.id_from_file[0],
                                                                 account_id=self.account_id)
            db.session.add(transaction)
            db.session.commit()
            db.session.flush(self.transaction)
            self.transaction = TransactionsTable.query.filter_by(verification_id=self.verification_id,
                                                                 amount=self.amount,
                                                                 id_from_file=self.id_from_file,
                                                                 account_id=self.account_id)
            return self.transaction

    def __init__(self,
                 verification_id,
                 id_from_file,
                 amount,
                 account_value,
                 vat,
                 reference_str=None, ):

        self.verification_id = int(verification_id),
        self.id_from_file = id_from_file,
        self.amount = amount,
        self.account_id = Accounting(account=account_value).if_account_new_save_it_in_db().id
        self.reference_str = Reference(reference_str=reference_str,account_id = self.account_id )
        self.vat = vat
        self.transaction = TransactionsTable.query.filter_by(verification_id=self.verification_id[0],
                                                             amount=self.amount[0],
                                                             id_from_file=self.id_from_file[0],
                                                             account_id=self.account_id).first()


class Transaction:
    def __init__(self, form_data=None, index=0, files=None):
        self.files = files
        self.form_data = form_data
        self.index = int(index)
        self.count_of_transactions = len(self.form_data.getlist('id'))

    @staticmethod
    def get_transaction_by_id(transaction_id: int):
        transaction: object = TransactionsTable.query.filter_by(name=transaction_id).first()
        return transaction

    @staticmethod
    def check_if_transaction_exist_in_db(id_from_file, date, amount, period) -> bool:
        transaction = TransactionsTable.query.filter_by(id_from_file=id_from_file,
                                                        date=date,
                                                        amount=amount,
                                                        period=period).first()
        if transaction is not None:
            return True
        else:
            return False

    def get_period_from_file(self) -> str:
        first_tr_date_in_list = self.form_data.getlist('date')[0]
        last_tr_date_in_list = self.form_data.getlist('date').pop()
        return f"""{first_tr_date_in_list} / {last_tr_date_in_list}"""

    def get_transaction_date_from_file(self) -> str:
        return self.form_data.getlist('date')[self.index]

    def get_transaction_amount_from_file(self) -> float:
        amount_string = self.form_data.getlist('amount')[self.index].replace(" ", "")
        return float(amount_string)

    @property
    def get_transaction_id_from_file(self):
        return self.form_data.getlist('id')[self.index]

    def update_transaktion(self):
        pass

    def if_transaction_new_save_it_in_db(self):
        period = f"""{self.form_data.getlist('date')[0]} / {self.form_data.getlist('date').pop()}"""
        company = Companies(bic=self.form_data.getlist('bic')[0], name=self.form_data.getlist('company_name')[0],
                            period=period).get_company()
        ref_string = self.form_data.getlist('reference')[self.index].upper()
        reference = Reference(reference_str=ref_string).if_reference_new_save_it_in_db()
        id_from_file = self.form_data.getlist('id')[self.index]
        date = self.form_data.getlist('date')[self.index]
        amount = float(self.form_data.getlist('amount')[self.index].replace(' ', ''))
        transaction = TransactionsTable(id_from_file=id_from_file,
                                        date=date,
                                        user=current_user.id,
                                        company_id=company.id,
                                        amount=amount,
                                        reference_id=reference.id,
                                        period=period)
        if self.check_if_transaction_exist_in_db(id_from_file, date, amount, period) is True:
            pass
            # # print("Transactions is not new")
        else:
            db.session.add(transaction)
            db.session.commit()
            # db.session.close()

    def update_reference_relationship_to_account(self):

        references_and_accounts = []
        for i in range(self.count_of_transactions):
            if self.form_data.getlist('account')[i] != '0':
                references_and_accounts.append(
                    (self.form_data.getlist('account')[i], self.form_data.getlist('reference')[i],
                     self.form_data.getlist('vat')[i]))

        clean_list = count(references_and_accounts)
        # print(f"""len of clean list: {len(clean_list)}""")

        for elem in clean_list:
            # print(elem)
            # print(f"""vat: {elem[0][2]} account: {elem[0][0]} reference: {elem[0][1]} count: {elem[1]}""")
            if elem[1] == 1:
                Reference(vat=elem[0][2], account=elem[0][0], reference_str=elem[0][1]).update_reference()

    def verification_file_update(self, transaction):

        if len(self.files[self.index].filename) != 0:
            file = self.files[self.index]
            transaction.file = save_transaction_file(file)

    def remove_verification_file(self, transaction):
        try:
            if self.form_data.getlist('remove_control')[self.index] == '1':
                remove_transaction_file(self.form_data['file_to_remove'])
                transaction.file = ''
        except IndexError:
            pass

    def add_comment(self, transaction):
        comment = self.form_data.getlist('comment')[self.index]
        transaction_comment = transaction.comment
        if transaction_comment != comment and comment != '':
            transaction.comment = comment

    def transaction_update(self):
        db_id = self.form_data.getlist('id')[self.index]
        vat = float(self.form_data.getlist('vat')[self.index].replace(' ', ''))
        transaction = TransactionsTable.query.filter_by(id=db_id).first()
        if vat != transaction.vat:
            transaction.vat = vat
        self.verification_file_update(transaction)
        self.remove_verification_file(transaction)
        self.add_comment(transaction)
        db.session.commit()
        # db.session.close()


class Reference:
    def __init__(self, reference_str='', description='', account_id=0, vat=0, ):
        reference_str = reference_str.replace("-", " ")
        reference_str = reference_str.replace(",", " ")
        reference_str = reference_str.replace(".", " ")
        self.reference_str = string_cleaner(reference_str.strip().upper())
        self.description = description
        # print(f"""{account} => {description}""")
        self.account_id = account_id


    def update_reference(self):
        reference = References.query.filter_by(reference_str=self.reference_str).first()
        print(f"""reference: {reference.reference_str}""")
        reference.account_id = self.account_id
        db.session.commit()

    def if_reference_new_save_it_in_db(self):
        print(self.reference_str)
        if References.query.filter_by(reference_str=self.reference_str.upper()).first() is None:
            reference = References(reference_str=self.reference_str, account_id=self.account_id)
            db.session.add(reference)
            db.session.commit()
            return reference
        else:
            self.update_reference()
            reference = References.query.filter_by(reference_str=self.reference_str).first()
            return reference

    def get_reference_by_reference_str_from_db(self):
        reference = References.query.filter_by(reference_str=self.reference_str).first()
        return reference


class Accounting:
    def __init__(self, account, vat=0, description=''):
        self.account = int(account)
        self.vat = float(vat)
        self.description = description

    def check_if_account_exist_in_db(self):
        account = Accounting_account.query.filter_by(account=self.account, vat=self.vat).first()
        if account is None:
            print(f"""account {account} in 'False'""")
            return False
        else:
            print(f"""account {account} in True""")
            return True

    def if_account_new_save_it_in_db(self):
        if self.check_if_account_exist_in_db() is False:
            account = Accounting_account(account=self.account, vat=self.vat, description=self.description)
            db.session.add(account)
            db.session.flush()
            return account
        else:
            account = Accounting_account.query.filter_by(account=self.account).first()
            return account

    def get_account_by_account_from_db(self):
        account = Accounting_account.query.filter_by(account=self.account).first()
        return account


class Transactions(Transaction):

    def if_transactions_new_save_it_to_db(self):
        for i in range(self.count_of_transactions):
            self.index = i
            self.if_transaction_new_save_it_in_db()

    def update_transaktions(self):
        for i in range(self.count_of_transactions):
            self.index = i
            self.transaction_update()
        self.update_reference_relationship_to_account()


def get_transactions_by_company_and_period(self, company_name: str, company_bic: int, period: str):
    result = [self.index]
    company = Companies(name=company_name, bic=company_bic).get_company()
    if company.user == current_user.id:
        transactions = company.transactions
        for transaction in transactions:
            if transaction.period == period:
                result.append(transaction)
    self.transactions = result


def count(listOfTuple):
    result = []
    import collections
    val = collections.Counter(listOfTuple)
    uniqueList = list(set(listOfTuple))
    print(uniqueList)
    for i in uniqueList:
        result.append((i, val[i]))
    return result


def save_transaction_file(file) -> str:
    new_file_name = create_uniq_file_name(secure_filename(file.filename))
    file.save(os.path.join(UPLOAD_FOLDER_FOR_TRANSACTIONS_FILES, new_file_name))
    return new_file_name
