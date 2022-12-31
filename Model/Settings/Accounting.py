# account
# description
# vat
from Model.DB import db
from Model.DataBase.Accounting_account import Accounting_account


class Account:
    def print_out(self):
        print(f"""{self.index}>>>{self.account_nr}>>>{self.description}""")

    def __init__(self, data, index):
        self.index = index
        self.data = data
        self.account_nr = data.getlist('account')[index]
        self.description = data.getlist('description')[index]
        self.vat = data.getlist('vat')[index]
        self.account_from_db = Accounting_account.query.filter_by(account=self.account_nr).first()

    def check_for_changes(self):
        if self.account_from_db is not None:
            if self.description != self.account_from_db.description:
                self.account_from_db.description = self.description
                db.session.commit()
            if self.vat != self.account_from_db.vat:
                self.account_from_db.vat = self.vat
                db.session.commit()
            if self.vat != self.account_from_db.vat:
                self.account_from_db.vat = self.vat
                db.session.commit()


    def update(self):
        self.print_out()
        return self


class Accounting:
    def print_out(self):
        print(self.data)

    def __init__(self, data):
        self.data = data
        self.count_of_accounts = len(data.getlist('account'))

    def update(self):
        for i in range(self.count_of_accounts):
            Account(data=self.data, index=i).check_for_changes()
