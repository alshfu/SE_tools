from flask import render_template

from Model.Company import Companies


def archive():
    companies = Companies()
    companies.print_loop_of_companies()
    return render_template("archive.html", result = companies.get_companies_list_from_db())