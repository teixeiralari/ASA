from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt 

class RegisterForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=50)])
    pwd = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6, max=50)
        ])
    confirm = PasswordField('Confirm password', [validators.EqualTo('pwd', message='Passwords do not match')])

class ArticleForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.DataRequired(), validators.Length(min=30)])
    