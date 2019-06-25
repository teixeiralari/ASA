from app import DB
from datetime import datetime

class Users(DB.Model):
    __tablename__ = 'users'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100))
    email = DB.Column(DB.String(100))
    username = DB.Column(DB.String(30))
    password = DB.Column(DB.String(100))
    register_date = DB.Column(DB.DateTime, default=datetime.now)

    def __init__(self, name=None, email=None, username=None, password=None):
        self.name = name
        self.email = email
        self.username = username
        self.password = password


class Articles(DB.Model):
    __tablename__ = 'articles'

    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(225))
    author = DB.Column(DB.String(100))
    body = DB.Column(DB.String())
    create_date = DB.Column(DB.DateTime, default=datetime.now)

    def __init__(self, title=None, author=None, body=None):
        self.title = title
        self.author = author
        self.body = body
