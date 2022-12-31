import os

from Model.DB import db
from Model.DataBase.Accounting_account import Accounting_account, References
from Model.DataBase.TransactionsTable import TransactionsTable
from Model.DataBase.Verifications import Verifications as VerificationDB
from config import UPLOAD_FOLDER, WORD_OF_EXCEPTIONS, get_list_of_stop_words
from functions.functions import allowed_file, create_uniq_file_name, remove_transaction_file


class Verification:
    @staticmethod
    def string_cleaner(ref_str='', is_float=False):
        reference = ref_str.replace('/', ' ')
        reference = reference.replace('_', ' ')
        reference = reference.replace(':', ' ')
        reference = reference.upper()
        reference = reference.strip()
        if is_float:
            reference = reference.replace(' ', '')
            reference = reference.replace(',', '.')
        else:
            reference = reference.replace('-', ' ')
            reference = reference.replace('.', ' ')
            reference = reference.replace(',', ' ')
        return reference

    def get_verification_from_db(self):
        verification = VerificationDB.query.filter_by(
            id=self.id,
            type_of_verifications=self.ver_type,
            date=self.date
        ).first()
        return verification

    def __init__(self, data, index, f_data):
        self.index = index
        self.file = f_data.files.getlist('file_of_verification')[index]
        self.file_list = f_data.files.getlist('file_of_verification')
        self.company = data.get('company')
        self.period = data.get('period')
        self.bic = data.get('bic')
        self.id = data.getlist('id')[index]
        self.id_from_file = data.getlist('id_from_file')[index]
        self.ver_type = data.getlist('type')[index]
        self.date = data.getlist('date')[index]
        self.base_account = data.getlist('base_account')[index]
        self.base_amount = float(self.string_cleaner(data.getlist('base_amount')[index], is_float=True))
        self.vat = float(self.string_cleaner(data.getlist('vat')[index], is_float=True))
        self.reference_string = data.getlist('reference_str')[index]
        self.list_of_transactions_id = data.getlist(f"""id_of_transaction_for_verifications_{index + 1}""")
        self.list_of_transactions_reference = data.getlist(f"""reference_of_transaction_for_verifications_{index + 1}""")
        self.list_of_transactions_amount = data.getlist(f"""amount_of_transaction_for_verifications_{index + 1}""")
        self.list_of_transactions_account = data.getlist(f"""account_of_transaction_for_verifications_{index + 1}""")

    def update(self):
        self.file_upload()
        self.clean_reference_of_verifications()
        self.check_reference_for_relation_with_account()
        self.check_for_similar_reference_of_verifications()
        self.update_account_of_second_transactions()
        self.update_vat()

    def check_for_similar_reference_of_verifications(self):
        account_id_reference = References.query.filter_by(reference_str=self.reference_string).first().account_id
        if account_id_reference is None and self.get_account_of_second_transaction() is None:
            for key_word in self.reference_string.split(' '):
                if key_word != '' and key_word not in get_list_of_stop_words() and len(key_word) > 2:
                    search = "%{}%".format(key_word)
                    references = References.query.filter(References.reference_str.ilike(search)).filter(References.account_id.isnot(None)).all()
                    if len(references) > 0:
                        # print(f"""id {self.id} => key_word  {key_word} => {self.reference_string} len of references {len(references)}""")
                        for reference in references:
                            account = Accounting_account.query.filter_by(id=reference.account_id).first()
                            if len(account.references) > 1:
                                print(f""" len of references {len(account.references)} id {self.id} => key_word  {key_word} => {self.reference_string} =>{account.description}""")
                                self.get_verification_from_db().transactions[1].account_id = account.id
                                db.session.commit()
                                break   # break for reference in references:

                        # print(f"""{reference.reference_str.lower()} => {reference.account_id} => {account.description}""")

    def check_reference_for_relation_with_account(self):
        reference = self.string_cleaner(self.reference_string)
        reference_from_db = References.query.filter_by(reference_str=self.reference_string).first()
        account_of_reference = Accounting_account.query.filter_by(id=reference_from_db.account_id).first()
        if account_of_reference is not None and self.get_account_of_second_transaction() is None:
            print(f"""id {self.id} {reference} => {reference_from_db.account_id} => {account_of_reference} """)
            self.get_verification_from_db().transactions[1].account_id = account_of_reference.id
            db.session.commit()

    def update_vat(self):
        if self.get_account_of_second_transaction() is not None:
            vat = self.get_verification_from_db().transactions[1].account.vat
            if vat != 0 and len(self.get_verification_from_db().transactions) == 2:
                print(f'''No VAT transaction''')
                self.add_vat_transaction()

    def clean_reference_of_verifications(self):
        if self.string_cleaner(self.reference_string) != self.get_verification_from_db().reference.reference_str:
            self.get_verification_from_db().reference.reference_str = self.string_cleaner(self.reference_string)
            db.session.commit()

    def add_vat_transaction(self):
        print(f"""amount of vat {self.calculate_vat_amount()} >> {self.calculate_ex_vat_amount()}""")
        print(self.get_verification_from_db().id)
        print(self.calculate_vat_amount())
        self.get_verification_from_db().transactions[1].amount = self.calculate_ex_vat_amount()
        transaction = TransactionsTable(
            account_id=Accounting_account.query.filter_by(account='2516').first().id,
            id_from_file=3,
            verification_id=self.get_verification_from_db().id,
            amount=self.calculate_vat_amount())
        db.session.add(transaction)
        db.session.commit()

    def file_upload(self):
        # print(f"""{self.index} => {self.file_list}""")
        if len(self.file.filename) != 0:
            if allowed_file(self.file.filename):
                filename = create_uniq_file_name(self.file.filename)
                self.file.save(os.path.join(UPLOAD_FOLDER, filename))
                self.get_verification_from_db().file = filename
                db.session.commit()

    def update_account_of_second_transactions(self):
        if len(self.base_account) == 4:
            if int(self.base_account) != self.get_account_of_second_transaction():
                print('Base account is not equal to second transaction account')
                print(self.base_account)
                print(self.get_account_of_second_transaction())
                print(self.get_verification_from_db().transactions[1].account)
                accounting = Accounting_account.query.filter_by(account=self.base_account).first()
                if self.get_verification_from_db().transactions[1].account is None:
                    print('Second transaction account is None')
                    self.get_verification_from_db().transactions[1].account = accounting
                    reference = References.query.filter_by(reference_str=self.reference_string).first()
                    reference.accounting_account = accounting
                    db.session.commit()
                else:
                    print('Second transaction account is not None')
                    print(f"""{accounting}>>{self.get_verification_from_db().reference.reference_str} >> {self.reference_string}""")
                    self.get_verification_from_db().transactions[1].account.account = self.base_account
                    reference = References.query.filter_by(reference_str=self.reference_string).first()
                    reference.account_id = self.get_verification_from_db().transactions[1].account.id
                    db.session.commit()

    def get_account_of_second_transaction(self):
        if self.get_verification_from_db().transactions[1].account is not None:
            return self.get_verification_from_db().transactions[1].account.account
        else:
            return self.get_verification_from_db().transactions[1].account

    def calculate_vat_amount(self):
        return round(self.base_amount - (self.base_amount / (1 + self.get_verification_from_db().transactions[1].account.vat)), 2)
        # vat_value.value = (ink_moms_value - (ink_moms_value / (1 + vat_rate))).toFixed(2);

    def calculate_ex_vat_amount(self):
        return round(self.base_amount / (1 + self.vat), 2)

    def print_out_verification(self):
        print(self.company)
        print(self.bic)
        print(self.period)
        print(self.get_verification_from_db())
        print(self.get_verification_from_db().id)
        print(self.get_verification_from_db().type_of_verifications)
        print(self.get_verification_from_db().id_from_file)
        print(self.get_verification_from_db().date)
        print(self.get_verification_from_db().period)
        print(self.get_verification_from_db().reference)
        print(self.get_verification_from_db().reference.account_id)
        print(self.get_verification_from_db().transactions)
        for tr in self.get_verification_from_db().transactions:
            print(tr.id)
            print(tr.amount)
            if tr.account is not None:
                print(tr.account.account)
                print(tr.account.description)


class Verifications:
    def __init__(self, data):
        self.data = data
        self.form_data = self.data.form

    def update(self):
        if "remove_file" in self.form_data:
            print(self.form_data.get("remove_file"))
            verification = VerificationDB.query.filter_by(id=self.form_data.get("remove_file")).first()
            remove_transaction_file(verification.file)
            verification.file = ''
            db.session.commit()
        else:
            count_of_verification = len(self.form_data.getlist('id'))
            for i in range(count_of_verification):
                Verification(index=i, data=self.form_data, f_data=self.data).update()

    def get_all_keys(self):
        keys = self.form_data.keys()
        for key in keys:
            if "account_of_transaction_for_verifications_" in key:
                pass
            elif "amount_of_transaction_for_verifications_" in key:
                pass
            elif "reference_of_transaction_for_verifications_" in key:
                pass
            elif "id_of_transaction_for_verifications_" in key:
                pass
            else:
                print(key)
