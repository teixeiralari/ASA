from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, text, select
from datetime import datetime

with open('/home/lariteixeira/ASA/password.txt') as f:
        password = f.read().strip()

class DbUtils:
    db = create_engine("postgresql+psycopg2://postgres:" + password + "@localhost/asa")
    metadados = MetaData(schema="myflaskapp")

    def users(self):
        users = Table('users', self.metadados, Column('id', Integer, primary_key=True),
        Column('name', String(100)), Column('email', String(100)), Column('username', String(30)),
        Column('password', String(100)), Column('register_date', DateTime, default=datetime.now),
        extend_existing=True)
        return users

    def articles(self):
        articles = Table('articles', self.metadados, Column('id', Integer, primary_key=True),
        Column('title', String(255)), Column('author', String(100)), Column('body', String()),
        Column('create_date', DateTime, default=datetime.now),
        extend_existing=True)
        return articles
    
    def new_user(self, name, email, username, password):
        users = self.users()
        self.conn = self.db.connect()
        self.conn.execute(users.insert(), name=name, email=email, username=username, password=password)
    
    def new_article(self, title, body, author):
        articles = self.articles()
        self.conn = self.db.connect()
        self.conn.execute(articles.insert(), title=title, body=body, author=author)
    
    def select_user(self, user):
        users = self.users()
        self.conn = self.db.connect()
        res = self.conn.execute(users.select().where(users.c.username == user)).first()
        return res
    
    def select_article_by_author(self, author):
        articles = self.articles()
        self.conn = self.db.connect()
        res = self.conn.execute(articles.select().where(articles.c.author == author)).fetchall()
        return res
    
    def select_article_by_id(self, id):
        articles = self.articles()
        self.conn = self.db.connect()
        res = self.conn.execute(articles.select().where(articles.c.id == id)).first()
        return res
    
    def select_all_articles(self):
        articles = self.articles()
        self.conn = self.db.connect()
        res = self.conn.execute(articles.select()).fetchall()
        return res
    
    def update_article(self, id, title, body):
        articles = self.articles()
        self.conn = self.db.connect()
        res = self.conn.execute(articles.update().where(articles.c.id == id).values(title=title, body=body))
    
    def delete_article(self, id):
        articles = self.articles()
        self.conn = self.db.connect()
        res = self.conn.execute(articles.delete().where(articles.c.id == id))
    