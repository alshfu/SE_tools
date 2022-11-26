def get_data_from_marginal_bank(data_string):
    transaktion_data_array = []
    line_array = data_string.splitlines()
    for i in range(len(line_array)):
        if i > 1:
            transaction = line_array[i].split(";")
            print(transaction)
            # print(transaction)
            transaktion_data_array.append({"id": i,
                                           "date": transaction[0],
                                           "reference": transaction[1].replace('"', ''),
                                           "amount": transaction[2].replace(',', '.'),
                                           "amount_in_account": transaction[3].replace(',', '.')})


    return transaktion_data_array[::-1]