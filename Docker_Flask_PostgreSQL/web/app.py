from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt 
from forms import *

from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from _config import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=POSTGRES_USER,
        passwd=POSTGRES_PASSWORD,
        host='172.20.0.2',
        port='5432',
        db=POSTGRES_DB)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the database connection
DB = SQLAlchemy(app)

from models import *

def db_initialization(dbstatus=True):
    while dbstatus:
        try:
            DB.create_all()
        except Exception as e:
            print('Create database failed ' + str(e))
        else:
            dbstatus = False
    

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():

    articles = Articles.query.all()
    
    if len(articles) > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('articles.html', msg=msg)

@app.route('/article/<string:id>/')
def article(id):
    
    #dbUtils = DbUtils()
    #article = dbUtils.select_article_by_id(id)
    article = Articles.query.filter(Articles.id == id).first()
    return render_template('article.html', article=article)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.pwd.data))

        #dbUtils = DbUtils()
        #dbUtils.new_user(name, email, username, password)

        user = Users(name, email, username, password)
        DB.session.add(user)
        DB.session.commit()
        flash('You are now registered and can log in', 'success')

        redirect(url_for('login'))
    return render_template('register.html', form=form) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        #get form fields
        username = request.form['username']
        possible_password = request.form['password']

        #dbUtils = DbUtils()
        #result = dbUtils.select_user(username)

        result = Users.query.filter(Users.username == username).first()
        #print(result.query.count())
        if (result):
            print(result)
            #Get stored hash
            password = result.password

            #Compare passwords
            if sha256_crypt.verify(possible_password, password):
                session['logged_in']=True
                session['username']=username
                
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


#check if the user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session: 
            return f(*args, **kwargs)
        else:
            flash('Unauthorized , please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    
    #dbUtils = DbUtils()
    #user = dbUtils.select_user(session['username'])
    #articles = dbUtils.select_article_by_author(user['name'])
    user = Users.query.filter(Users.username == session['username']).first()
    articles = Articles.query.filter(Articles.author == user.name)
    
    if articles:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('dashboard.html', msg=msg)

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_articles():

    #dbUtils = DbUtils()
    #user = dbUtils.select_user(session['username'])
    user = Users.query.filter(Users.username == session['username']).first()

    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        #dbUtils.new_article(title, body, user['name'])
        new_article = Articles(title, user.name, body)
        DB.session.add(new_article)
        DB.session.commit()

        flash('Article created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_articles(id):

    #dbUtils = DbUtils()
    #article = dbUtils.select_article_by_id(id)
    article = Articles.query.filter(Articles.id == id).first()

    form = ArticleForm(request.form)

    form.title.data = article.title
    form.body.data = article.body

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        
        article = Articles.query.filter(Articles.id == id).first()
        article.title = title
        article.body = body
        #dbUtils.update_article(id, title, body)
        DB.session.commit()

        flash('Article update', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)

@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    
    #dbUtils = DbUtils()
    #dbUtils.delete_article(id)
    Articles.query.filter(Articles.id == id).delete()
    DB.session.commit()

    flash('Article deleted', 'success')
    return redirect(url_for('dashboard'))

if __name__=='__main__':
    db_initialization()
    app.secret_key='secret_key'
    app.run(debug=True, host='0.0.0.0')
