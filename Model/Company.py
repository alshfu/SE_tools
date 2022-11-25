from flask_login import current_user

from Model.DB import db
from functions.functions import remove_transaction_file


class Companies:

    def remove_company_period(self):
        print(f"""remove company with id: {self.name} and period: {self.period}""")
        from Model.DataBase.Company import Companies
        company = Companies.query.filter_by(name=self.name, bic=self.bic).first()
        transactions = company.transactions
        company_user = company.user
        if company_user == current_user.id:
            print(f"""Company from db query: {self.company.name} with BIC {self.company.bic}""")
            print(f"""company_user: {self.user} | current_user: {self.user.id}""")
            db.session.delete(company)
            for transaction in transactions:
                if transaction.period == self.period and company_user == current_user.id:
                    remove_transaction_file(transaction.file)
                    print(f"""period: {self.period} | {transaction.period}""")
                    print(transaction)
                    db.session.delete(transaction)
            db.session.commit()

    def get_transaction_for_company_and_period(self):
        return self.company.transactions

    def print_loop_of_company_transaction(self):
        print("transaktions loop")
        for transaktion in self.get_transaction_for_company_and_period():
           print(transaktion)

    def get_companies_list_from_db(self):
        print(self.companies)
        return self.companies

    def print_loop_of_companies(self):
        for company in self.companies:
            print(company.transactions)

    def save_company_in_db_if_new(self):
        if self.companies_query.filter_by(bic=self.bic, period=self.period).first() is not None:
            print("company is not new")
            self.company = self.companies_query.filter_by(bic=self.bic, period=self.period).first()
        else:
            print("company is new")
            self.user = current_user
            self.bic = self.bic
            self.name = self.name
            self.period = self.period
            db.session.add(self.company)
            db.session.commit()
            db.session.flush()
            self.company = self.companies_query.filter_by(bic=self.bic, period=self.period).first()

    def get_company(self):
        self.save_company_in_db_if_new()
        return self.company

    def __init__(self, period=None, name=None, bic=None):

        self.period = period
        self.name = name
        self.bic = bic
        self.user = current_user
        from Model.DataBase.Company import Companies
        self.companies = Companies.query.all()
        self.company = Companies(name=self.name, bic=self.bic, period=self.period)
        self.companies_query = db.session.query(Companies)
