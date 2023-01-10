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

def read_csv_from_swedbank_to_byte_and_return_utf_string(csv_file):
    # å = \xc3\xa5 b'\xe5'
    byte_array = []
    try:
        with open(csv_file, "rb") as f:
            while byte := f.read(1):
                # å = \xc3\xa5 b'\xe5'
                if byte == b'\xe5':
                    byte = b'\xc3\xa5'
                # Å = \xc3\x85 b'\xc5'
                elif byte == b'\xc5':
                    byte = b'\xc3\x85'
                # ö = \xc3\xb6 b'\xf6'
                elif byte == b'\xf6':
                    byte = b'\xc3\xb6'
                # Ö = \xc3\x96 b'\xd6'
                elif byte == b'\xd6':
                    byte = b'\xc3\x96'
                # ä = \xc3\xa4 b'\xe4'
                elif byte == b'\xe4':
                    byte = b'\xc3\xa4'
                # Ä = \xc3\x84 b'\xc4'
                elif byte == b'\xc4':
                    byte = b'\xc3\x84'
                elif byte == b'\x96':
                    byte = b''
                byte_array.append(byte)

            # Do stuff with byte.
    except IOError:
        pass

    utf_string = ""

    for i in range(len(byte_array)):
        try:
            utf_string += byte_array[i].decode("utf-8")
            # print(utf_string)
        except UnicodeDecodeError:
            pass

    return utf_string


