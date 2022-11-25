import os


from flask_login import current_user
from werkzeug.utils import secure_filename

from Model.DB import db
from Model.DataBase.Company import Companies
from Model.DataBase.TransactionsTable import TransactionsTable
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER_FOR_TRANSACTIONS_FILES


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_csv_to_byte_return_utf(csv_file):
    # å = \xc3\xa5 b'\xe5'
    byte_array = []
    try:
        with open(csv_file, "rb") as f:
            while byte := f.read(1):
                # å = \xc3\xa5 b'\xe5'
                if byte == b'\xe5':
                    byte = b'\xc3\xa5'
                    # byte = b'å'
                # Å = \xc3\x85 b'\xc5'
                elif byte == b'\xc5':
                    byte = b'\xc3\x85'
                    # byte = b'Å'
                # ö = \xc3\xb6 b'\xf6'
                elif byte == b'\xf6':
                    byte = b'\xc3\xb6'
                    # byte = b'ö'
                # Ö = \xc3\x96 b'\xd6'
                elif byte == b'\xd6':
                    byte = b'\xc3\x96'
                    # byte = b'Ö'
                # ä = \xc3\xa4 b'\xe4'
                elif byte == b'\xe4':
                    byte = b'\xc3\xa4'
                # Ä = \xc3\x84 b'\xc4'
                elif byte == b'\xc4':
                    byte = b'\xc3\x84'
                    # byte = b'Ä'
                elif byte == b'\x96':
                    byte = b''
                byte_array.append(byte)
            # Do stuff with byte.
    except IOError:
        print('Error While Opening the file!')

    utf_string = ""
    for i in range(len(byte_array)):
        utf_string += byte_array[i].decode("utf-8")
    # print(f"""{i}:{byte_array[i]}:{byte_array[i].hex()}:{byte_array[i].decode("utf-8")}""")
    return utf_string


def get_data_from_swedbank(data_string):
    transaktion_data_array = []
    line_array = data_string.splitlines()
    for i in range(len(line_array)):
        if i > 1:
            transaction = line_array[i].split(",")

            if len(transaction) != 12:
                correct_value = transaction[8:-3]
                first_array = transaction[:8]
                last_array = transaction[-3:]
                correct_string = ' '.join([str(elem) for elem in correct_value])
                first_array.append(correct_string)
                for elem in last_array: first_array.append(elem)
                transaction = first_array
            # print(transaction)
            transaktion_data_array.append({"id": transaction[0],
                                           "date": transaction[7],
                                           "reference": transaction[8].replace('"', ''),
                                           "amount": transaction[10],
                                           "amount_in_account": transaction[11]})
    return transaktion_data_array[::-1]


def amount_counter(transaktions_array):
    resultat = 0
    for i in range(len(transaktions_array)):
        try:
            amount_on_account = float(transaktions_array[i]['amount_in_account'])
            amount = float(transaktions_array[i + 1]['amount'])
            resultat = amount_on_account + amount
        except IndexError:
            pass
    return str(resultat)


def remove_transaction_file(file_name):
    if file_name != '':
        full_file_path = f"""{UPLOAD_FOLDER_FOR_TRANSACTIONS_FILES}/{file_name}"""

        if os.path.exists(full_file_path):
            os.remove(full_file_path)
        else:
            print("Nothing to remove !!")
    return ""








def create_uniq_file_name(file_name='') -> str:
    import hashlib
    from datetime import datetime
    file_extension = file_name.split('.').pop().lower()
    f_name_hash = hashlib.sha256()
    file_name_to_save = hashlib.sha256()
    time_now_hash = hashlib.sha256()
    file_name = file_name.encode('utf-8')
    time_now = str(datetime.now()).encode('utf-8')
    f_name_hash.update(file_name)
    time_now_hash.update(time_now)
    f_name_hash.digest()
    time_now_hash.digest()
    file_name_to_save.update(f"""{f_name_hash.hexdigest()}_{time_now_hash.hexdigest()}""".encode('utf-8'))
    file_name_to_save.digest()
    return f"""{str(file_name_to_save.hexdigest())}.{file_extension}"""







def remove_transaction_file(file_name):
    print("remove_transaction_file for file: ", file_name)
    if file_name != '':
        full_file_path = f"""{UPLOAD_FOLDER_FOR_TRANSACTIONS_FILES}/{file_name}"""
        print(full_file_path)
        if os.path.exists(full_file_path):
            os.remove(full_file_path)
        else:
            print("Nothing to remove !!")
    return ""
