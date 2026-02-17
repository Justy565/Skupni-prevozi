from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'fortnite'

db = TinyDB('db.json')
user_table = db.table('users')
voznje_table = db.table('voznje')


@app.context_processor
def inject_globals():
    # da lahko v vseh template-ih uporabljas datetime in session
    return dict(datetime=datetime)


# OSNOVNA
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('home.html')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()

            if not username or not password:
                return jsonify({'success': False, 'error': 'Uporabniško ime in geslo sta obvezna.'})

            UserQ = Query()
            if user_table.get(UserQ.username == username):
                return jsonify({'success': False, 'error': 'Uporabniško ime je že zasedeno.'})

            user_table.insert({'username': username, 'password': password})
            return jsonify({'success': True})

        except Exception as e:
            print("Napaka register:", e)
            return jsonify({'success': False, 'error': 'Prišlo je do napake med registracijo.'})

    return render_template('register.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()

            if not username or not password:
                return jsonify({'success': False, 'error': 'Uporabniško ime in geslo sta obvezna.'})

            User = Query()
            user = user_table.search(User.username == username)

            if not user:
                return jsonify({'success': False, 'error': 'Uporabnik ne obstaja. Najprej se registriraj.'})

            if user[0]['password'] != password:
                return jsonify({'success': False, 'error': 'Napačno geslo.'})

            session['username'] = username
            session['user_id'] = user[0].doc_id
            return jsonify({'success': True})

        except Exception as e:
            print("Napaka login:", e)
            return jsonify({'success': False, 'error': 'Prišlo je do napake.'})

    return render_template('login.html')


# DASHBOARD
@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


# DODAJ VOZNJO
@app.route('/dodaj_voznjo', methods=['GET', 'POST'])
def dodaj_voznjo():
    if 'user_id' not in session:
        if request.method == 'POST':
            return jsonify({'success': False, 'error': 'Nisi prijavljen'}), 401
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            data = request.get_json(force=True)

            required = ['zacetek', 'destinacija', 'datum', 'cas', 'cena', 'sedezi', 'telefonska']
            for k in required:
                if k not in data or str(data[k]).strip() == '':
                    return jsonify({'success': False, 'error': f'Manjka polje: {k}'}), 400

            voznje_table.insert({
                'user_id': session['user_id'],
                'zacetek': data['zacetek'],
                'destinacija': data['destinacija'],
                'datum': data['datum'],
                'cas': data['cas'],
                'cena': data['cena'],
                'sedezi': data['sedezi'],
                'telefonska': data['telefonska']
            })
            return jsonify({'success': True})

        except Exception as e:
            print("Napaka dodaj_voznjo:", e)
            return jsonify({'success': False, 'error': 'Prišlo je do napake pri shranjevanju.'}), 500

    return render_template('dodaj_voznjo.html')


# API MOJE VOZNJE
@app.route('/api/moje_voznje')
def api_moje_voznje():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Ni prijave'}), 401

    records = voznje_table.search(Query().user_id == session['user_id'])
    voznje = [{'doc_id': doc.doc_id, **doc} for doc in records]
    return jsonify({'success': True, 'voznje': voznje})


# MOJE VOZNJE
@app.route('/moje_voznje')
def moje_voznje():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('moje_voznje.html')


# VOZNJE DRUGIH
@app.route('/vse_voznje')
def vse_voznje():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    vse = voznje_table.search(Query().user_id != session['user_id'])
    return render_template('vse_voznje.html', voznje=vse)


# IZBRIS
@app.route('/izbrisi_voznjo/<int:voznja_id>', methods=['POST'])
def izbrisi_voznjo(voznja_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Nisi prijavljen'}), 401

    voznja = voznje_table.get(doc_id=voznja_id)
    if not voznja:
        return jsonify({'success': False, 'error': 'Vožnja ne obstaja'})

    if voznja.get('user_id') != session['user_id']:
        return jsonify({'success': False, 'error': 'Dostop zavrnjen'}), 403

    voznje_table.remove(doc_ids=[voznja_id])
    return jsonify({'success': True})


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
