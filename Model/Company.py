from flask_login import current_user

from Model.DB import db
from functions.functions import remove_transaction_file
from Model.DataBase.Company import Companies as CompanyDB


class Companies:

    def remove_company_period(self):
        print(f"""remove company with id: {self.name} and period: {self.period}""")
        company = CompanyDB.query.filter_by(name=self.name, bic=self.bic).first()
        transactions = company.verifications
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

    def get_verifications_for_company_and_period(self):
        return self.company.verifications

    def print_loop_of_company_transaction(self):
        print("transaktions loop")
        for transaktion in self.get_verifications_for_company_and_period():
            print(transaktion)

    def get_companies_list_from_db(self):
        #print(self.companies)
        return self.companies

    def print_loop_of_companies(self):
        print(self.company)

    def save_company_in_db_if_new(self):
        if self.companies_query.filter_by(bic=self.bic, period=self.period, name=self.name).first() is not None:
            #print("company is not new")
            self.company = self.companies_query.filter_by(bic=self.bic, name=self.name).first()
        else:
           # print("company is new")
            self.user = current_user
            self.bic = self.bic
            self.name = self.name
            db.session.add(self.company)
            db.session.commit()
            db.session.flush()
            self.company = self.companies_query.filter_by(bic=self.bic, name=self.name).first()

    def get_company(self):
        self.save_company_in_db_if_new()
        return self.company

    def __init__(self, name=None, bic=None, period=None):
        self.period = period
        self.name = name
        self.bic = bic
        self.user = current_user
        from Model.DataBase.Company import Companies
        self.companies = Companies.query.all()
        self.company = Companies(name=self.name, bic=self.bic, period=self.period)
        self.companies_query = db.session.query(Companies)
