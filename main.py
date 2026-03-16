from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)
app.secret_key = "fortnite"

db = TinyDB("db.json")
users = db.table("users")
voznje = db.table("voznje")


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("index"))
    return render_template("home.html")


@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")


@app.route("/mnenja")
def mnenja():
    return render_template("mnenja.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "" or password == "":
            return jsonify({"success": False, "error": "Uporabniško ime in geslo sta obvezna."})

        User = Query()
        obstaja = users.get(User.username == username)

        if obstaja:
            return jsonify({"success": False, "error": "Uporabniško ime že obstaja."})

        users.insert({
            "username": username,
            "password": password
        })

        return jsonify({"success": True})

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "" or password == "":
            return jsonify({"success": False, "error": "Uporabniško ime in geslo sta obvezna."})

        User = Query()
        user = users.get(User.username == username)

        if not user:
            return jsonify({"success": False, "error": "Uporabnik ne obstaja."})

        if user["password"] != password:
            return jsonify({"success": False, "error": "Napačno geslo."})

        session["user_id"] = user.doc_id
        session["username"] = user["username"]

        return jsonify({"success": True})

    return render_template("login.html")


@app.route("/index")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/dodaj_voznjo", methods=["GET", "POST"])
def dodaj_voznjo():
    if "user_id" not in session:
        if request.method == "POST":
            return jsonify({"success": False, "error": "Nisi prijavljen."})
        return redirect(url_for("login"))

    if request.method == "POST":
        data = request.get_json()

        danes = datetime.now().date()
        izbran_datum = datetime.strptime(data["datum"], "%Y-%m-%d").date()

        if izbran_datum < danes:
            return jsonify({
                "success": False,
                "error": "Ne moreš dodati vožnje za nazaj."
            })

        voznje.insert({
            "user_id": session["user_id"],
            "zacetek": data["zacetek"],
            "destinacija": data["destinacija"],
            "datum": data["datum"],
            "cas": data["cas"],
            "cena": data["cena"],
            "sedezi": data["sedezi"],
            "telefonska": data["telefonska"]
        })

        return jsonify({"success": True})

    return render_template("dodaj_voznjo.html")


@app.route("/api/moje_voznje")
def api_moje_voznje():
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Nisi prijavljen."})

    moje = voznje.search(Query().user_id == session["user_id"])
    seznam = []

    for v in moje:
        en = dict(v)
        en["doc_id"] = v.doc_id
        seznam.append(en)

    return jsonify({"success": True, "voznje": seznam})


@app.route("/moje_voznje")
def moje_voznje():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("moje_voznje.html")


@app.route("/vse_voznje")
def vse_voznje():
    if "user_id" not in session:
        return redirect(url_for("login"))

    vse = voznje.search(Query().user_id != session["user_id"])
    return render_template("vse_voznje.html", voznje=vse)


@app.route("/izbrisi_voznjo/<int:id>", methods=["POST"])
def izbrisi_voznjo(id):
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Nisi prijavljen."})

    voznja = voznje.get(doc_id=id)

    if not voznja:
        return jsonify({"success": False, "error": "Vožnja ne obstaja."})

    if voznja["user_id"] != session["user_id"]:
        return jsonify({"success": False, "error": "Nimaš dostopa."})

    voznje.remove(doc_ids=[id])
    return jsonify({"success": True})


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)