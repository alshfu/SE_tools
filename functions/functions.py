import os

from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





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
        full_file_path = f"""{UPLOAD_FOLDER}/{file_name}"""
        if os.path.exists(full_file_path):
            os.remove(full_file_path)
        else:
            pass
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

def string_cleaner(ref_str='', is_float=False):
    reference = ref_str.replace('/', ' ')
    reference = reference.replace('_', ' ')
    reference = reference.replace(':', ' ')
    reference = reference.replace('"', '')
    reference = reference.replace("'", '')
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
