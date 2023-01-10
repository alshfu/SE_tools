import datetime
import os

from Model.Archive.Verification import Verification
from Model.DataBase.Accounting_account import Accounting_account


class Verification_of_SE_file(Verification):

    def __init__(self, data, index, f_data):
        super().__init__(data, index, f_data)
        self.index = index

    def transactions_string(self):
        string = ""
        count_of_transactions = len(self.list_of_transactions_id)
        for i in range(count_of_transactions):
            if len(self.list_of_transactions_account[i]) == 0:
                string += f"#TRANS 2290 {{}} {self.list_of_transactions_amount[i]}  \"\" \"\" 0\n"
            else:
                string += f"#TRANS {self.list_of_transactions_account[i]} {{}} {self.list_of_transactions_amount[i]} "" "" \"\" \"\" 0\n"
        return string

    def verification_string(self):
        first_line = f"""#VER {self.ver_type} {self.index + 1} {self.date} "{self.reference_string}" {self.date}\n"""
        second_line = "{\n"
        transactions_lines = self.transactions_string()
        last_lines = "}\n\n"
        return first_line + second_line + transactions_lines + last_lines


class SE_File:
    @staticmethod
    def create_list_of_accounts():
        accounts = Accounting_account.query.all()
        accounts_list = []
        for account in accounts:
            accounts_list.append(f"""#KONTO {account.account} "{account.description}"\n""")
        return accounts_list
    def __init__(self, data, f_data):
        self.f_data = f_data
        self.data = data
        print(self.data.get('period'))

    def head_of_file(self):
        period = self.data.get('period').replace('-', '').replace(' ', '').replace('/', ' ').split(' ')
        first_line = f"""#FLAGGA 1\n"""
        second_line = f"""#\n"""
        third_line = f"""#PROGRAM Visma eEkonomi 7.5.0.19919\n"""
        fourth_line = f"""#FORMAT PC8\n"""
        fifth_line = f"""#GEN {datetime.datetime.now().strftime('%Y%m%d')} {self.data.get('name')}\n"""
        sixth_line = f"""#SIETYP 4\n"""
        seventh_line = f"""#ORGNR {self.data.get('bic')}\n"""
        eighth_line = f"""#FNAMN \"{self.data.get('name')}\"\n"""
        ninth_line = f"""#RAR 0 {period[1]} {period[0]}\n"""
        tenth_line = f"""#KPTYP EUBAS97\n"""
        eleventh_line = f"""#VALUTA SEK\n"""
        twelfth_line = f"""#\n"""

        return first_line + second_line + third_line + fourth_line + fifth_line + sixth_line + seventh_line + eighth_line + ninth_line + tenth_line + \
            eleventh_line + twelfth_line

    def create_se_file(self):
        directory = f"""{os.getcwd()}/downloads"""
        file_name = f"SE_file_{self.data.get('name')}_{self.data.get('period')}.se".replace('/', '_').replace(' ', '')
        with open(f"""{directory}/{file_name}""", 'w') as fp:
            fp.write(self.head_of_file())
            for account_string in self.create_list_of_accounts():
                fp.write(account_string)
            count_of_verifications = len(self.data.getlist('id'))
            for index in range(count_of_verifications):
                verification = Verification_of_SE_file(self.data, index, self.f_data)
                fp.write(verification.verification_string())

        return file_name
