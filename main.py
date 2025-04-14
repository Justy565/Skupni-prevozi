from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from tinydb import TinyDB, Query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


db = TinyDB('db.json')
user_table = db.table('users')

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    UserQuery = Query()
    user = user_table.get(UserQuery.id == int(user_id))
    if user:
        return User(user_id=user['id'], username=user['username'], password=user['password'])
    return None


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Enter username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)],
                             render_kw={"placeholder": "Enter password"})
    submit = SubmitField('Register')

    
    def validate_username(self, username):
        existing_user = user_table.search(Query().username == username.data)
        if existing_user:
            raise ValidationError('Ta username je ze v uporabi')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Vnesi username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)],
                             render_kw={"placeholder": "Vnesi geslo"})
    submit = SubmitField('Login')




if __name__ == '__main__':
    app.run(debug=True)
