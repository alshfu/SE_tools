def get_data_from_marginal_bank(data_string):
    transaktion_data_array = []
    line_array = data_string.splitlines()
    for i in range(len(line_array)):
        if i > 0:
            transaction = line_array[i].split(";")
            # print(transaction)
            # print(transaction)
            transaktion_data_array.append({"id": i,
                                           "date": transaction[0],
                                           "reference": transaction[1].replace('"', ''),
                                           "amount": transaction[2].replace(',', '.'),
                                           "amount_in_account": transaction[3].replace(',', '.')})

    return transaktion_data_array


def read_csv_from_marginal_to_byte_and_return_utf_string(csv_file):
    # å = \xc3\xa5 b'\xe5'
    byte_array = []
    try:
        with open(csv_file, "rb") as f:
            file_byte_string = f.read(1)
            # print(file_byte_string)
            print(len(file_byte_string))

            while byte := f.read(1):
                #    # å = \xc3\xa5 b'\xe5'
                #    if byte == b'\xe5':
                #        byte_array[i] = b'\xc3\xa5'
                #        # byte_array[i] = b'å'
                #    # Å = \xc3\x85 b'\xc5'
                #    elif byte == b'\xc5':
                #        byte_array[i] = b'\xc3\x85'
                #        # byte_array[i] = b'Å'
                #    # ö = \xc3\xb6 b'\xf6'
                #    elif byte == b'\xf6':
                #        byte_array[i] = b'\xc3\xb6'
                #        # byte_array[i] = b'ö'
                #    # Ö = \xc3\x96 b'\xd6'
                #    elif byte == b'\xd6':
                #        byte_array[i] = b'\xc3\x96'
                #        # byte_array[i] = b'Ö'
                #    # ä = \xc3\xa4 b'\xe4'
                #    elif byte == b'\xe4':
                #        byte_array[i] = b'\xc3\xa4'
                #    # Ä = \xc3\x84 b'\xc4'
                #    elif byte == b'\xc4':
                #        byte_array[i] = b'\xc3\x84'
                #        # byte_array[i] = b'Ä'
                #    elif byte == b'\x96':
                #        byte_array[i] = b''
                byte_array.append(byte)
            # Do stuff with byte.
    except IOError:
        pass

    utf_string = ""

    for i in range(len(byte_array)):
        try:
            if byte_array[i] == b'\xe5' and byte_array[i + 1] == b'\xa5':
                #byte_array[i] = b'\xc3\xa5'
                byte_array[i] = b'\xc3\x85'
            #        # byte_array[i] = b'å'
            #    # Å = \xc3\x85 b'\xc5'
            elif byte_array[i] == b'\xc3' and byte_array[i + 1] == b'\x85':
                byte_array[i] = b'\xc3\x85'
            #        # byte_array[i] = b'Å'
            #    # ö = \xc3\xb6 b'\xf6'
            elif byte_array[i] == b'\xc3' and byte_array[i + 1] == b'\xb6':
                #byte_array[i] = b'\xc3\xb6'
                byte_array[i] = b'\xc3\x96'
            #        # byte_array[i] = b'ö'
            #    # Ö = \xc3\x96 b'\xd6'
            elif byte_array[i] == b'\xc3' and byte_array[i + 1] == b'\x96':
                byte_array[i] = b'\xc3\x96'
            #        # byte_array[i] = b'Ö'
            #    # ä = \xc3\xa4 b'\xe4'
            elif byte_array[i] == b'\xc3' and byte_array[i + 1] == b'\xa4':
                    #byte_array[i] = b'\xc3\xa4'
                    byte_array[i] = b'\xc3\x84'
            #    # Ä = \xc3\x84 b'\xc4'
            elif byte_array[i] == b'\xc3' and byte_array[i + 1] == b'\x84':
                    byte_array[i] = b'\xc3\x84'
            #        # byte_array[i] = b'Ä'
            print(byte_array[i])
            utf_string += byte_array[i].decode("utf-8")
        # print(utf_string)
        except UnicodeDecodeError:
            pass


    return utf_string
