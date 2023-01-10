from flask import Flask, redirect

from Controller.UserProfile.logout import user_logout
from Model.DB import db
from Model.DataBase.Accounting_account import Accounting_account
from views.archive import archive
from views.game_of_king import game_of_king
from views.home_page import index
from views.csv_to_se import csv_to_se
from views.login import login_manager
from views.login import login
from views.se_file_reader import se_file_reader
from views.se_tools import se_tools
from views.settings_accounting import settings_accounting
from views.show_transaction_file import show_transaction_file
from views.verifications import verifications

app = Flask(__name__)
app.config.from_pyfile('config.py')
login_manager.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.context_processor
def context():
    return {"menu": [
        ["Home", "/"],
        ["Archive", "/archive"],
        ["CSV läsare", "/csv_to_se"],
        ["SE Redigerare", "/se_file_reader"],
        ["Settings", "/settings", [
            ["Konto inställningar", "/settings/accounting"]
        ]
         ]

    ],
        "accounting": Accounting_account.query.all()
    }


app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=user_logout, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/verifications', view_func=verifications, methods=['GET', 'POST'])
app.add_url_rule('/csv_to_se', view_func=csv_to_se, methods=['GET', 'POST'])
app.add_url_rule('/se_file_reader', view_func=se_file_reader, methods=['GET', 'POST'])
app.add_url_rule('/archive', view_func=archive, methods=['GET', 'POST'])
app.add_url_rule('/settings/accounting', view_func=settings_accounting, methods=['GET', 'POST'])
app.add_url_rule('/se_tools', view_func=se_tools, methods=['GET', 'POST'])
app.add_url_rule('/uploads/', view_func=show_transaction_file, methods=['GET', 'POST'])
app.add_url_rule('/game_of_king/', view_func=game_of_king, methods=['GET', 'POST'])


# app.add_url_rule('/client_profile', view_func=client_profile, methods=['GET', 'POST'])
# app.add_url_rule('/logout', view_func=logout)

@app.errorhandler(401)
def custom_401(error):
    print(error)
    return redirect('/login')


if __name__ == '__main__':
    app.run()
