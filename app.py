from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "semma_angical"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cadastros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_animal TEXT,
        raca TEXT,
        idade TEXT,
        tutor TEXT,
        cpf TEXT,
        telefone TEXT,
        endereco TEXT,
        bairro TEXT,
        foto TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["usuario"]
        senha = request.form["senha"]

        if user == "admin" and senha == "1234":
            session["user"] = user
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM cadastros")
    total = c.fetchone()[0]
    conn.close()

    return render_template("dashboard.html", total=total)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        dados = request.form
        foto = request.files["foto"]

        nome_foto = foto.filename
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_foto))

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""INSERT INTO cadastros 
        (nome_animal, raca, idade, tutor, cpf, telefone, endereco, bairro, foto)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (dados["nome"], dados["raca"], dados["idade"],
         dados["tutor"], dados["cpf"], dados["telefone"],
         dados["endereco"], dados["bairro"], nome_foto))
        conn.commit()
        conn.close()

        return redirect("/lista")

    return render_template("cadastro.html")

@app.route("/lista")
def lista():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cadastros")
    dados = c.fetchall()
    conn.close()

    return render_template("lista.html", dados=dados)

app.run(debug=True)
