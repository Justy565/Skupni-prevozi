from flask import Flask, render_template, redirect, url_for, request, session
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'osnovni_secret'

db = TinyDB('db.json')
user_table = db.table('users')
voznje_table = db.table('voznje')

#osnovna stran
@app.route('/')
def home():
    return render_template('home.html')

#registracija
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        UserQ = Query()
        if user_table.get(UserQ.username == username):
            return 'Uporabniško ime je že zasedeno.'
        new_id = len(user_table) + 1
        user_table.insert({'id': new_id, 'username': username, 'password': password})
        return redirect(url_for('login'))
    return render_template('register.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        UserQ = Query()
        user = user_table.get(UserQ.username == username and UserQ.password == password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        return 'Napačno uporabniško ime ali geslo.'
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
