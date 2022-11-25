import os
from flask import render_template, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from Model.Transactions import Transactions
from config import UPLOAD_FOLDER
from functions.functions import allowed_file
from functions.functions import get_data_from_swedbank
from functions.functions import read_csv_to_byte_return_utf
from functions.functions import amount_counter

@login_required
def csv_to_se():
    if request.method == 'POST' and "transactions_list_from_file" in request.form:
        print("len of form request: ",len(request.form))
        Transactions(form_data=request.form, ).if_transactions_new_save_it_to_db()
        return render_template("csv_to_se.html")
    elif request.method == 'POST' and request.files['csv_file']:
        file = request.files['csv_file']
        if file and allowed_file(file.filename):
            file_data = [1, 2, 3]
            filename = secure_filename(file.filename)
            print("csv file was uploaded")
            print(filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            transaktions_array = get_data_from_swedbank(read_csv_to_byte_return_utf(UPLOAD_FOLDER + "/" + filename))
            start_amount = transaktions_array[0]["amount_in_account"]
            end_amount = amount_counter(transaktions_array)
            return render_template("csv_to_se.html",
                                   end_amount=end_amount,
                                   result=transaktions_array,
                                   start_amount=start_amount)
    elif request.method == 'GET':
        return render_template("csv_to_se.html")
