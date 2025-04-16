from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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
            raise ValidationError('Ta username je že v uporabi')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Vnesi username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)],
                             render_kw={"placeholder": "Vnesi geslo"})
    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_query = Query()
        user = user_table.get(user_query.username == form.username.data)
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            user_obj = User(user_id=user['id'], username=user['username'], password=user['password'])
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            form.password.errors.append('Nepravilno uporabniško ime ali geslo')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_id = len(user_table) + 1
        user_table.insert({'id': new_id, 'username': form.username.data, 'password': hashed_password})
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
