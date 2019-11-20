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
    comment_text = db.Column('comment_text', db.String(280))
    sentiment_label = db.Column('sentiment', db.String(3))
    sentiment_score = db.Column('sentiment_score', db.Float())

    # twitter id

    def __init__(self, show, comment_text, label, score):
        self.show_id = show
        self.comment_text = comment_text
        self.sentiment_label = label
        self.sentiment_score = score



# class Queries(db.Model):
#     """keep track of tiwtter quieries made"""
#     pass

# date
# num results
# queries ran
# last twitter id
# show if#d
