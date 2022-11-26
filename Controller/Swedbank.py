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
