from Model.Transactions_from_SE_file import Reference, Accounting

MAIN_ACCOUNT = 1930


def read_se_file_to_byte_and_get_utf_string(csv_file):
    # å = \xc3\xa5 b'\xe5'
    byte_array = []
    try:
        with open(csv_file, "rb") as f:
            while byte := f.read(1):
                print(byte)
                # å = \xc3\xa5
                if byte == b'\x86':
                    byte = b'\xc3\xa5'
                # Å = \xc3\x85
                elif byte == b'\x8f':
                    byte = b'\xc3\x85'
                # ö = \xc3\xb6
                elif byte == b'\x94':
                    byte = b'\xc3\xb6'
                # Ö = \xc3\x96
                elif byte == b'\x99':
                    byte = b'\xc3\x96'
                # ä = \xc3\xa4
                elif byte == b'\x84':
                    byte = b'\xc3\xa4'
                # Ä = \xc3\x84
                elif byte == b'\x8e':
                    byte = b'\xc3\x84'
                #############################
                elif byte == b'\xe2':
                    byte = b' '
                byte_array.append(byte)
            # Do stuff with byte.
    except IOError:
        pass

    utf_string = ""

    for i in range(len(byte_array)):
        try:
            utf_string += byte_array[i].decode("utf-8")
        except UnicodeDecodeError:
            pass
    return get_data_from_SE_fil(utf_string)


def get_reference_from_se_file(index_of_begin=None, spliter_string=None, index_of_end=None) -> str:
    spliter_string = spliter_string[index_of_begin:index_of_end]
    reference_str = ''
    for x in range(len(spliter_string)):
        reference_str += spliter_string[x] + ' '
    return reference_str


def get_data_from_SE_fil(data_string):
    list_of_verifications = []
    line_array = data_string.splitlines()
    bic = '',
    company_name = '',
    period = ''
    for i in range(len(line_array)):
        spliter_string = line_array[i].split(' ')
        # print(f"""for i {i} {spliter_string}""")
        if spliter_string[0] == '#ORGNR':
            bic = spliter_string[1]
            print(f'''Bic: {bic}''')
        elif spliter_string[0] == '#FNAMN':
            company_name = get_reference_from_se_file(spliter_string=spliter_string, index_of_begin=1)
            print(f"""Företag namn: {company_name}""")
        elif spliter_string[0] == '#RAR':
            first_date = spliter_string[2][:4] + '-' + spliter_string[2][4:6] + '-' + spliter_string[2][6:8]
            last_date = spliter_string[3][:4] + '-' + spliter_string[3][4:6] + '-' + spliter_string[3][6:8]
            period = first_date + ' / ' + last_date
        elif spliter_string[0] == '#KONTO':
            account_value = spliter_string[1]
            reference_str = get_reference_from_se_file(spliter_string=spliter_string, index_of_begin=2)
            account_id = Accounting(account=account_value, description=reference_str).if_account_new_save_it_in_db().id
            Reference(account_id=account_id,
                      description=reference_str,
                      reference_str=reference_str).if_reference_new_save_it_in_db()
        elif spliter_string[0] == '#VER':
            verification_id = spliter_string[2]
            verification_type = spliter_string[1]
            verification_date = spliter_string[3][:4] + '-' + spliter_string[3][4:6] + '-' + spliter_string[3][6:8]
            verification_reference = get_reference_from_se_file(spliter_string=spliter_string, index_of_begin=4, index_of_end=-1)
            transactions = []
            if '#TRANS' == line_array[i + 2].split(' ')[0]:
                trans_count = 2
                while '#TRANS' == line_array[i + trans_count].split(' ')[0]:
                    transactions_array = line_array[i + trans_count].split(' ')
                    transaction_account = transactions_array[1]
                    transaction_amount = float(transactions_array[3])
                    transaction_reference = ''
                    if len(transactions_array) > 4:
                        transaction_reference = get_reference_from_se_file(spliter_string=transactions_array, index_of_begin=5)
                    transactions.append({'transaction_account': transaction_account,
                                         'transaction_amount': transaction_amount,
                                         'transaction_reference': transaction_reference})

                    trans_count += 1

            verification = {'verification_id': verification_id,
                            'period_of_verification': period,
                            'verification_type': verification_type,
                            'verification_date': verification_date,
                            'verification_reference': verification_reference,
                            'transactions': transactions
                            }

            list_of_verifications.append(verification)

    return bic, company_name, list_of_verifications
