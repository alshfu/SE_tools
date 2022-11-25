from flask import render_template, request, send_from_directory

from config import UPLOAD_FOLDER_FOR_TRANSACTIONS_FILES


def show_transaction_file():
    if request.method == "GET":
        file = send_from_directory(UPLOAD_FOLDER_FOR_TRANSACTIONS_FILES,request.args['file_name'])
        print(file)
        # return render_template('transaktion_list/transaction_file_popup.html', result = file)
        return file
    #TODO: create error message