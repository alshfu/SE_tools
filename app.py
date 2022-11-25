from flask import Flask, redirect

from Model.DB import db
from views.archive import archive
from views.home_page import index
from views.csv_to_se import csv_to_se
from views.login import login_manager
from views.login import login
from views.se_tools import se_tools
from views.show_transaction_file import show_transaction_file
from views.transactions_view import transactions_view

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
        ["SE Redigerare", "/se_editor"],
        ["Settings", "/settings"]
    ]
    }


app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
app.add_url_rule('/csv_to_se', view_func=csv_to_se, methods=['GET', 'POST'])
app.add_url_rule('/archive', view_func=archive, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/se_tools', view_func=se_tools, methods=['GET', 'POST'])
app.add_url_rule('/se_tools/transaktions_list', view_func=transactions_view, methods=['GET', 'POST'])
app.add_url_rule('/uploads/transactions_files/', view_func=show_transaction_file, methods=['GET', 'POST'])


# app.add_url_rule('/client_profile', view_func=client_profile, methods=['GET', 'POST'])
# app.add_url_rule('/logout', view_func=logout)

@app.errorhandler(401)
def custom_401(error):
    print(error)
    return redirect('/login')


if __name__ == '__main__':
    app.run()
