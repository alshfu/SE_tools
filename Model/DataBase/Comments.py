from datetime import datetime

from flask_login import current_user
from sqlalchemy import Sequence

from Model.DB import db



class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    comment = db.Column(db.String())
    date_and_time = db.Column(db.String())
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



    def __init__(self, comment):

        self.comment = comment
        self.date_and_time = str(datetime.now())
        self.user = current_user