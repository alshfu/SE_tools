
from sqlalchemy import Sequence


from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    login_name = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    active = False
    anonymous = False

    def __init__(self, login_name, password):
        self.login_name = login_name
        self.password = password

    def is_active(self):
        """
        """
        self.active = True
        return self.active

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        self.anonymous = False
        return self.anonymous
