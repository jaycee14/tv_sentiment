from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Shows(db.Model):
    """docstring for Shows"""

    id = db.Column('show_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    service = db.Column('service', db.String(20))
    active = db.Column('active', db.Boolean())

    def __init__(self, name, service, active):
        self.name = name
        self.service = service
        self.active = active


class Comments(db.Model):
    """model for shows"""

    id = db.Column('message_id', db.Integer, primary_key=True)
    show_id = db.Column('show_id', db.Integer)
    comment_text = db.Column('comment_text', db.String(300))
    sentiment_label = db.Column('sentiment', db.String(3))
    sentiment_score = db.Column('sentiment_score', db.Float())
    model_used = db.Column('model_used', db.String(100))
    query_id = db.Column('query_id', db.Integer)
    comment_date = db.Column('comment_date_utc', db.DateTime)


    def __init__(self, show, comment_text, label, score, model, query, comment_date):
        self.show_id = show
        self.comment_text = comment_text
        self.sentiment_label = label
        self.sentiment_score = score
        self.model_used = model
        self.query_id = query
        self.comment_date = comment_date


class Queries(db.Model):
    """keep track of twitter queries made"""

    id = db.Column('query_id', db.Integer, primary_key=True)
    query_date = db.Column('query_date', db.DateTime)
    show_id = db.Column('show_id', db.Integer)
    last_extract_id = db.Column('last_extract_id', db.BigInteger)
    query_string = db.Column('query_string', db.String(120))

    def __init__(self, show_id, last_id, query_string):
        self.query_date = datetime.now()
        self.show_id = show_id
        self.last_extract_id = last_id
        self.query_string = query_string


