import os
from flask import render_template, request, redirect
from flask_login import login_required
from werkzeug.utils import secure_filename

from Controller.Marginal import get_data_from_marginal_bank, read_csv_from_marginal_to_byte_and_return_utf_string
from Controller.Swedbank import get_data_from_swedbank, read_csv_from_swedbank_to_byte_and_return_utf_string
from Model.Transactions_from_SE_file import Transactions
from Model.Verifications_from_csv_file import Verifications
from config import UPLOAD_FOLDER
from functions.functions import allowed_file
from functions.functions import amount_counter


@login_required
def csv_to_se():
    if request.method == 'POST' and "transactions_list_from_file" in request.form:
        print("create nwe verifications from csv file ")
        Verifications(form_data=request.form).create_verifications_from_csv()
        company_name = (request.form.get('company_name'))
        company_bic = (request.form.get('bic'))
        period = f"""{request.form.getlist('date')[0]} / {request.form.getlist('date').pop()}"""
        str_of_render = f"""/verifications?company_name={company_name}&company_bic={company_bic}&period={period}&verifications_list=true"""
        return redirect(str_of_render)
    elif request.method == 'POST' and request.files['csv_file']:
        file = request.files['csv_file']
        if file and allowed_file(file.filename):
            transaktions_array: list
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            if request.form.getlist('bank')[0] == '2':  # Swedbank
                transaktions_array = get_data_from_swedbank(
                    read_csv_from_swedbank_to_byte_and_return_utf_string(UPLOAD_FOLDER + "/" + filename))
            elif request.form.getlist('bank')[0] == '5':  # Marginal
                transaktions_array = get_data_from_marginal_bank(
                    read_csv_from_marginal_to_byte_and_return_utf_string(UPLOAD_FOLDER + "/" + filename))
            start_amount = transaktions_array[0]["amount_in_account"]
            end_amount = amount_counter(transaktions_array)

            return render_template("csv_reader/csv_to_se.html",
                                   end_amount=end_amount,
                                   result=transaktions_array,
                                   start_amount=start_amount)
    elif request.method == 'GET':
        return render_template("csv_reader/csv_to_se.html")
