from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from tinydb import TinyDB, Query
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'fortnite'

db = TinyDB('db.json')
user_table = db.table('users')
voznje_table = db.table('voznje')

#osnovna stran
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('index'))
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
                    session['user_id'] = user[0].doc_id 
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
    return render_template('index.html')



#dodaj voznje
@app.route('/dodaj_voznjo', methods=['GET', 'POST'])
def dodaj_voznjo():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Nisi prijavljen'}), 401

    if request.method == 'POST':
        data = request.get_json()
        voznje_table.insert({
            'user_id': session['user_id'],
            'zacetek': data['zacetek'],
            'destinacija': data['destinacija'],
            'datum': data['datum'],
            'cas': data['cas'],
            'cena': data['cena'],
            'sedezi': data['sedezi']
        })
        return jsonify({'success': True})

    return render_template('dodaj_voznjo.html')

@app.route('/api/moje_voznje')
def api_moje_voznje():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Ni prijave'}), 401
    moje = voznje_table.search(Query().user_id == session['user_id'])
    return jsonify({'success': True, 'voznje': moje})


#pregled svojih vozenj
@app.route('/moje_voznje')
def moje_voznje():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    moje = voznje_table.search(Query().user_id == session['user_id'])
    return render_template('moje_voznje.html', voznje=moje)

@app.route('/vse_voznje')
def vse_voznje():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    User = Query()
    vse = voznje_table.search(User.user_id != session['user_id'])
    return render_template('vse_voznje.html', voznje=vse)

#odjava
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
