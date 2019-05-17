from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from sqlalchemy import create_engine
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt 
from forms import *
from db_config import myconfig
from functools import wraps


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    db = create_engine(myconfig)
    query = "select * from myflaskapp.articles"
    articles = db.execute(query)
    if articles is not None:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('articles.html', msg=msg)

@app.route('/article/<string:id>/')
def article(id):
    db = create_engine(myconfig)
    query = "select * from myflaskapp.articles where id = %s"
    article = db.execute(query, [id]).fetchone()
    return render_template('article.html', article=article)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.pwd.data))

        db = create_engine(myconfig)
        query = "insert into myflaskapp.users(name, email, username, password) VALUES (%s, %s, %s, %s)"
        values = (name, email, username, password)
        db.execute(query, values)
        flash('You are now registered and can log in', 'success')

        redirect(url_for('login'))
    return render_template('register.html', form=form) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        #get form fields
        username = request.form['username']
        possible_password = request.form['password']

        db = create_engine(myconfig)
        query = "select * from myflaskapp.users where username = %s"
        values = [username]
        result = db.execute(query, values).fetchone()
        
        if (result is not None) and (len(result) > 0):
            #Get stored hash
            password = result['password']

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
    db = create_engine(myconfig)
    query = "select name from myflaskapp.users where username=%s"
    values = [session['username']]
    user = db.execute(query, values).fetchone()


    db = create_engine(myconfig)
    query = "select * from myflaskapp.articles where author = %s"
    values = user['name']
    articles = db.execute(query, values)

    if articles is not None:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('dashboard.html', msg=msg)

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_articles():
    db = create_engine(myconfig)
    query = "select name from myflaskapp.users where username=%s"
    values = [session['username']]
    user = db.execute(query, values).fetchone()

    print(user['name'])
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        
        print(body)
        db = create_engine(myconfig)
        query = "insert into myflaskapp.articles(title, body, author) VALUES (%s, %s, %s)"
        values = (title, body, user['name'])
        db.execute(query, values)
        flash('Article created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_articles(id):
    db = create_engine(myconfig)
    query = "select * from myflaskapp.articles where id = %s"
    article = db.execute(query, [id]).fetchone()

    form = ArticleForm(request.form)

    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        
        db = create_engine(myconfig)
        query = "update myflaskapp.articles set title=%s, body=%s where id=%s"

        values = (title, body, id)
        db.execute(query, values)
        flash('Article update', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)

@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    db = create_engine(myconfig)
    query = "delete from myflaskapp.articles where id=%s"
    db.execute(query, [id])

    flash('Article deleted', 'success')
    return redirect(url_for('dashboard'))

if __name__=='__main__':
    app.secret_key='secret_key'
    app.run(debug=True)