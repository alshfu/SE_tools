import flask
from flask import request
from flask import redirect
from flask_login import login_user, LoginManager, logout_user

from Model.DataBase.User import User
from app import db

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


def login():
    if User.query.filter_by(login_name='admin').first() is None:
        admin = User(login_name="admin", password="zu5ba5o")
        db.session.add(admin)
        db.session.commit()
    else:
        pass
        #create_simple_transaction()

    if request.method == "POST":
        login_from_form = request.form["login"]
        psw_from_form = request.form["password"]
        if len(login_from_form) != 0 and len(psw_from_form) != 0:
            user = User.query.filter_by(login_name=request.form["login"]).first()
            print(user.id)
            print(user.password)
            print(user.login_name+" == "+login_from_form)

            if user is not None and user.login_name == login_from_form:
                if user.password == psw_from_form:
                    login_user(user)
                    return redirect("/")
        else:
            print("No pws or login in form")

    return flask.render_template("login_page.html")


def logout():
    logout_user()
    return redirect("/login")
