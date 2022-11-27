'''This file contains DB tables modeling'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UnlabeledData(db.Model):
    """
    unlabeled_data table:
    we store all text data users send to our application
    """
    __tablename__ = "unlabeled_data"
    id = db.Column(db.Integer, primary_key=True)
    raw_text_input = db.Column(db.String(10000000),
                               unique=True, nullable=False)
    model_output = db.Column(db.String(10000000))

    def __init__(self, raw_text_input: str, model_output: str):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.raw_text_input = raw_text_input
        self.model_output = model_output
