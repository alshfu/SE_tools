from flask import request, render_template, redirect

from Model.Company import Companies
from Model.Archive.Verifications_from_archive import Verifications

def verifications():
    if request.method == "GET":
        if "verifications_list" in request.args:
            company_name = request.args.get('company_name')
            period = request.args.get('period')
            company_bic = request.args.get('company_bic')
            #print(f"""Company name is {company_name} bic = {company_bic} period = {period}""")
            company = Companies(name=company_name, bic=company_bic, period=period).get_company()
            return render_template("verifications_list/main.html", result=company)
    elif request.method == "POST":
        if "search_box" in request.form:
            company = Companies(name=request.form.get("name"),
                                bic=request.form.get("bic"),
                                period=request.form.get("period")).get_company()
            print(request.form.get("search_box"))
            print(company)
            return render_template("verifications_list/main.html", result=company, search_box=request.form.get("search_box"))
    Verifications(data=request).update()
    return redirect(request.referrer)
