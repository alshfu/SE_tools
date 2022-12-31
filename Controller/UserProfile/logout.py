from flask import redirect
from flask_login import login_required, logout_user


@login_required
def user_logout():
    logout_user()
    return redirect("/")