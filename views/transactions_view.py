from flask import render_template, request, redirect

from Model.Company import Companies

from Model.Transactions_from_SE_file import Transactions, Accounting


def transactions_view():
    if request.method == "GET":
        # print(request.args)
        if "transaktions_list" in request.args:
            if request.args.get('transaktions_list') == "true":
                # print("remove_company is in request")
                company_name = request.args.get('company_name')
                period = request.args.get('period')
                bic = request.args.get('company_bic')
                print("""hire is deklaration of company""")
                company = Companies(name=company_name, bic=bic, period=period)
                company.get_company()
                transactions = company.get_transaction_for_company_and_period()
                return render_template("transaktion_list/transactions_header.html",
                                       company_name=company_name,
                                       period=period,
                                       company_bic=bic,
                                       result=transactions)
        return render_template("transaktion_list/transactions_header.html")
    elif request.method == "POST":
        if "transactions_update" in request.form:
            print("request form is transactions update")
            Transactions(form_data=request.form, files = request.files.getlist("tr_file")).update_transaktions()
        elif "search_form" in request.form:
            transactions_res = []
            search_value = request.form.get("search_input")
            if Accounting(account=search_value).get_account_by_account_from_db() is not None:
                search_in_accounting_result = Accounting(account=search_value).get_account_by_account_from_db().references
                if search_in_accounting_result is not None:
                    print(f"""Search result in accounting: {search_in_accounting_result}""")
                    for reference in search_in_accounting_result:
                        reference_transactions = reference.transactions
                        for transaction in reference_transactions:
                            print(f"""period: {request.form.get("period")} | company: {request.form.get("company_name")}""")
                            if transaction.period == request.form.get("period") and transaction.company.name == request.form.get("company_name"):
                                transactions_res.append(transaction)
                                print(f"""Search result for transaction: {transaction}""")
                    print(f"""Search for: {search_value}""")
                    return render_template("transaktion_list/transactions_header.html",
                                           company_name=request.form.get("company_name"),
                                           period=request.form.get("period"),
                                           result=transactions_res)


        return redirect(request.referrer)
    else:
        return render_template("transaktion_list/transactions_header.html")
