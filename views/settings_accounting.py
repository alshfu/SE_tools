from flask import render_template, request, redirect

from Model.DataBase.Accounting_account import Accounting_account
from Model.Settings.Accounting import Accounting


def settings_accounting():
    if request.method == "POST":
        print("Verifications update is hire")
        Accounting(data=request.form).update()
        return redirect(request.referrer)
    else:
        result = Accounting_account.query.all()
        return render_template("settings/settings_accounting.html", result=result)
