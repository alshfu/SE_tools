from Model.Company import Companies
from Model.DB import db
from Model.DataBase.Verifications import Verifications as verifications_table
from Model.Transactions_from_SE_file import Reference, Transaction_from_se_file, Accounting


class Verifications:
    def __init__(self, form_data, index=0, files=None):
        self.period = form_data.get('period')
        self.company_id = Companies(bic=form_data.get('bic'), period=self.period, name=form_data.get('company_name')).get_company().id
        self.len_of_form_data = len(form_data.getlist('ver_id'))
        self.files = files
        self.index = int(index)
        self.form_data = form_data

    def get_list_from_form(self, string):
        return self.form_data.getlist(string)

    def get_transactions(self, index, verification):

        tr_reference_name_string = f"""tr_reference_of_ver_{index + 1}"""
        tr_account_of_ver_name_string = f"""tr_account_of_ver_{index + 1}"""
        tr_amount_of_ver_name_string = f"""tr_amount_of_ver_{index + 1}"""
        print(f"""verification_id {verification.id} index {index + 1}""")
        verification_id = verification.id
        tr_ref_list = self.get_list_from_form(tr_reference_name_string)
        tr_acc_list = self.get_list_from_form(tr_account_of_ver_name_string)
        tr_amo_list = self.get_list_from_form(tr_amount_of_ver_name_string)
        count_of_transactions = len(self.get_list_from_form(tr_amount_of_ver_name_string))

        for i in range(count_of_transactions):
            tr_index = i
            try:
                reference_str = tr_ref_list[i]
            except IndexError:
                reference_str = ''

            Transaction_from_se_file(verification_id=verification_id,
                                     id_from_file=tr_index,
                                     amount=float(tr_amo_list[i]),
                                     account_value=int(tr_acc_list[i]),
                                     reference_str=reference_str,
                                     vat=0).get_transaction()

    def save_verification_to_db(self, index):
        if self.check_if_verification_exist(index) is False:
            reference = Reference(reference_str=self.get_list_from_form('ver_reference')[index])
            reference.if_reference_new_save_it_in_db()
            reference_id = reference.get_reference_by_reference_str_from_db().id

            verification = verifications_table(
                reference_id=reference_id,
                type_of_verifications=self.get_list_from_form('ver_type')[index],
                company_id=self.company_id,
                id_from_file=self.get_list_from_form('ver_id')[index],
                period=self.period,
                date=self.get_list_from_form('ver_date')[index],
            )
            db.session.add(verification)
            db.session.flush()
            # print(verification.id)
            tr_account_of_ver_name_string = f"""tr_account_of_ver_{index + 1}"""
            self.get_transactions(index=index, verification=verification)
            account_value = int(self.get_list_from_form(tr_account_of_ver_name_string)[1])
            # reference.get_reference_by_reference_str_from_db().account_id = Accounting(account=account_value).if_account_new_save_it_in_db().id
            Reference(reference_str=self.get_list_from_form('ver_reference')[index],
                      account_id=Accounting(account=account_value).if_account_new_save_it_in_db().id).update_reference()
            db.session.commit()
            return verification

    def check_if_verification_exist(self, index):
        verification = verifications_table.query.filter_by(
            type_of_verifications=self.get_list_from_form('ver_type')[index],
            company_id=self.company_id,
            id_from_file=self.get_list_from_form('ver_id')[index],
            date=self.get_list_from_form('ver_date')[index],
        ).first()
        if verification is None:
            return False
        else:
            return True

    def save_verifications_if_new(self):
        for index in range(self.len_of_form_data):
            verification = ''
            if self.check_if_verification_exist(index) is False:
                verification = self.save_verification_to_db(index)
            else:
                verification = self.save_verification_to_db(index)

    def print_out_verifikation(self, index):
        print(
            f"""{index} | {self.form_data.getlist('ver_id')[index]}| {self.form_data.getlist('ver_type')[index]}| {self.form_data.getlist('ver_date')[index]}| {self.form_data.getlist('ver_reference')[index]}""")
