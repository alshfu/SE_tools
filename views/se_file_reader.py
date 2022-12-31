import os

from flask import render_template, request
from werkzeug.utils import secure_filename

from Controller.SE_files import read_se_file_to_byte_and_get_utf_string

from Model.Verifications_from_SE_file import Verifications
from config import UPLOAD_FOLDER
from functions.functions import allowed_file


def se_file_reader():
    if request.method == 'POST' and "se_file_submit" in request.form:
        print(f"""file submit is hire""")
        file = request.files['se_file']
        print(f"""se_file: {file}""")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            data_from_se_file = read_se_file_to_byte_and_get_utf_string(UPLOAD_FOLDER + "/" + filename)
            return render_template("se_reader/se_reader.html", result=data_from_se_file)
    elif request.method == 'POST' and "verification_list" in request.form:
        Verifications(request.form).save_verifications_if_new()
        return render_template("se_reader/se_reader.html")
    return render_template("se_reader/se_reader.html")