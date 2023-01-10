from flask import render_template, request

from Model.Company import Companies


def archive():
    if request.method == "GET":
        if "remove_company_period" in request.args:
            print("remove_company_period")
            company_name = request.args.get('name')
            period = request.args.get('period')
            company_bic = request.args.get('bic')
            Companies(name=company_name, bic=company_bic, period=period).remove_company_period()
    companies = Companies()
    return render_template("archive.html", result = companies.get_companies_list_from_db())