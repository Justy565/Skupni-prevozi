from flask import Flask, render_template, redirect, url_for, request, session, jsonify
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
        try:
            username = request.form['username']
            password = request.form['password']

            UserQ = Query()
            existing_user = user_table.get(UserQ.username == username)

            if existing_user:
                return jsonify({'success': False, 'error': 'Uporabniško ime je že zasedeno.'})

            user_table.insert({'username': username, 'password': password})
            return jsonify({'success': True})

        except Exception as e:
            print(f"Napaka pri registraciji: {str(e)}")
            return jsonify({'success': False, 'error': 'Prišlo je do napake med registracijo.'})

    return render_template("register.html")


#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            User = Query()
            user = user_table.search(User.username == username)
            if user:
                if user[0]['password'] == password:
                    session['username'] = username
                    return jsonify({'success': True})
                else:
                    return jsonify({'success': False, 'error': 'Wrong password'})
            else:
                return jsonify({'success': False, 'error': 'User not found. Please sign up.'})
        except Exception as e:
            print(f"Napaka pri prijavi: {str(e)}")
            return jsonify({'success': False, 'error': 'Prišlo je do napake'})
    return render_template("login.html")

#glavna stran
@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return f"Pozdravljen {session['username']}! <a href='/dodaj_voznjo'>Dodaj vožnjo</a> | <a href='/moje_voznje'>Moje vožnje</a> | <a href='/logout'>Odjava</a>"

#dodaj voznje
@app.route('/dodaj_voznjo', methods=['GET', 'POST'])
def dodaj_voznjo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        zacetek = request.form.get('zacetek')
        destinacija = request.form.get('destinacija')
        datum = request.form.get('datum')
        sedezi = request.form.get('sedezi')
        voznje_table.insert({
            'user_id': session['user_id'],
            'zacetek': zacetek,
            'destinacija': destinacija,
            'datum': datum,
            'sedezi': sedezi
        })
        return redirect(url_for('moje_voznje'))
    return render_template('dodaj_voznjo.html')

#pregled svojih vozenj
@app.route('/moje_voznje')
def moje_voznje():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    moje = voznje_table.search(Query().user_id == session['user_id'])
    return render_template('moje_voznje.html', voznje=moje)

#odjava
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
