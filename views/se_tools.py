from flask import redirect, request

from Model.Company import Companies


def se_tools():
    if request.method == "GET":
        #print(request.args)
        if "remove_company_period" in request.args:
            if request.args.get('remove_company_period') == "true":
                #print("remove_company is in request")
                company_name = request.args.get('company_name')
                period = request.args.get('period')
                bic = request.args.get('company_bic')
                #print("company name: ", company_name," and period: ",period)
                Companies(name=company_name,period=period, bic=bic).remove_company_period()
    return redirect(request.referrer)