from flask import render_template, request, send_from_directory

from config import UPLOAD_FOLDER

def show_transaction_file():
    print("show_transaction_file")
    if request.method == "GET":
        file = send_from_directory(UPLOAD_FOLDER,request.args['file_name'])
        print("file")
        # return render_template('transaktion_list/transaktions_search.html', result = file)
        return file
    #TODO: create error message