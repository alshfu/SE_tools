from flask import render_template, request, redirect

from Model.Company import Companies
from Model.Transactions import Transactions


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
                return render_template("transaktion_list/transactions_view.html",
                                       company_name=company_name,
                                       period=period,
                                       company_bic=bic,
                                       result=transactions)
        return render_template("transaktion_list/transactions_view.html")
    elif request.method == "POST":
        print("request method is POST")
        Transactions(form_data=request.form, files = request.files.getlist("tr_file")).update_transaktions()

        return redirect(request.referrer)
    else:
        return render_template("transaktion_list/transactions_view.html")
