from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from tinydb import TinyDB, Query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

db = TinyDB('db.json')
user_table = db.table('users')
voznje_table = db.table('voznje')

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, user_id, username, password, is_admin=False):
        self.id = user_id
        self.username = username
        self.password = password
        self.is_admin = is_admin


@login_manager.user_loader
def load_user(user_id):
    UserQuery = Query()
    user = user_table.get(UserQuery.id == int(user_id))
    if user:
        return User(user_id=user['id'], username=user['username'], password=user['password'],
                    is_admin=user.get('is_admin', False))
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


class VoznjaForm(FlaskForm):
    destination = StringField(validators=[InputRequired(), Length(min=3, max=50)],
                              render_kw={"placeholder": "Destinacija"})
    date = DateField(validators=[InputRequired()], render_kw={"placeholder": "Datum"})
    seats = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Št. mest"})
    submit = SubmitField('Dodaj vožnjo')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # Admin
        if form.username.data == 'admin' and form.password.data == 'admin123':
            admin = User(user_id=0, username='admin', password='admin123', is_admin=True)
            login_user(admin)
            return redirect(url_for('admin_nadzor'))

        # Navaden
        user_query = Query()
        user = user_table.get(user_query.username == form.username.data)
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            user_obj = User(
                user_id=user['id'],
                username=user['username'],
                password=user['password'],
                is_admin=user.get('is_admin', False)
            )
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


@app.route('/dodaj_voznjo', methods=['GET', 'POST'])
@login_required
def dodaj_voznjo():
    form = VoznjaForm()
    if form.validate_on_submit():
        voznje_table.insert({
            'user_id': current_user.id,
            'destination': form.destination.data,
            'date': str(form.date.data),
            'seats': form.seats.data
        })
        return redirect(url_for('moje_voznje'))
    return render_template('dodaj_voznjo.html', form=form)


@app.route('/moje_voznje')
@login_required
def moje_voznje():
    user_voznje = voznje_table.search(Query().user_id == current_user.id)
    return render_template('moje_voznje.html', voznje=user_voznje)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def admin_nadzor():
    if not current_user.is_admin:
        return "Dostop zavrnjen"
    vsi_uporabniki = user_table.all()
    return render_template('admin.html', uporabniki=vsi_uporabniki)


if __name__ == '__main__':
    app.run(debug=True)
