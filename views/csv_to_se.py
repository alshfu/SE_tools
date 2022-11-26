import os
from flask import render_template, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from Controller.Marginal import get_data_from_marginal_bank
from Controller.Swedbank import get_data_from_swedbank
from Model.Transactions import Transactions
from config import UPLOAD_FOLDER
from functions.functions import allowed_file
from functions.functions import read_csv_to_byte_return_utf
from functions.functions import amount_counter

@login_required
def csv_to_se():
    if request.method == 'POST' and "transactions_list_from_file" in request.form:
        # # print("len of form request: ",len(request.form))
        Transactions(form_data=request.form, ).if_transactions_new_save_it_to_db()
        return render_template("csv_to_se.html")
    elif request.method == 'POST' and request.files['csv_file']:
        file = request.files['csv_file']
        if file and allowed_file(file.filename):
            transaktions_array : list
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            if request.form.getlist('bank')[0] == '2': # Swedbank
                transaktions_array = get_data_from_swedbank(read_csv_to_byte_return_utf(UPLOAD_FOLDER + "/" + filename))
            elif request.form.getlist('bank')[0] == '5': # Marginal
                transaktions_array = get_data_from_marginal_bank(read_csv_to_byte_return_utf(UPLOAD_FOLDER + "/" + filename))
            start_amount = transaktions_array[0]["amount_in_account"]
            end_amount = amount_counter(transaktions_array)





            return render_template("csv_to_se.html",
                                   end_amount=end_amount,
                                   result=transaktions_array,
                                   start_amount=start_amount)
    elif request.method == 'GET':
        return render_template("csv_to_se.html")
