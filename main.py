from flask import Flask, request, jsonify

app = Flask(__name__)

uporabniki = []
voznje = []


@app.route('/registracija', methods=['POST'])
def registracija():
    podatki = request.json
    ime = podatki.get("ime")

    if ime in uporabniki:
        return jsonify({"sporocilo": "Uporabnik že obstaja!"}),

    uporabniki.append(ime)
    return jsonify({"sporocilo": "Registracija uspešna!", "uporabniki": uporabniki})



if __name__ == '__main__':
    app.run(debug=True)
