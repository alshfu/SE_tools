import os

from flask import send_from_directory, current_app, send_file

from Model.Archive.create_se_file import SE_File
from Model.DB import db
from Model.DataBase.Verifications import Verifications as VerificationDB
from functions.functions import  remove_transaction_file
from Model.Archive.Verification import Verification
from Model.Archive.download_seldected import Verification_to_download


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
        elif "download_selected" in self.form_data:
            count_of_verification = len(self.form_data.getlist('id'))
            for i in range(count_of_verification):
                Verification_to_download(index=i, data=self.form_data, f_data=self.data).get_selected()
        elif "create_se_file" in self.form_data:
            se_file = SE_File(data=self.form_data, f_data=self.data).create_se_file()
            directory = f"""{os.getcwd()}/downloads"""
            path = f"""{directory}/{se_file}"""
            return send_file(path_or_file=path, as_attachment=True)
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
