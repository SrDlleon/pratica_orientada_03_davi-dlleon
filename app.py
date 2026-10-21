from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select

from database import SessionLocal, init_db
from models import Book, User

app = Flask(__name__)
init_db()


@app.get("/")
def index():
    session = SessionLocal()
    usuarios = session.scalars(select(User).order_by(User.nome)).all()
    livros = session.scalars(select(Book).order_by(Book.titulo)).all()
    return render_template("index.html", usuarios=usuarios, livros=livros)


@app.route("/usuarios/novo", methods=["GET", "POST"])
def users_new():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()

        if nome and email:
            session = SessionLocal()
            existente = session.scalar(select(User).where(User.email == email))
            if not existente:
                session.add(User(nome=nome, email=email))
                session.commit()
            return redirect(url_for("index"))

    return render_template("user_form.html")


@app.route("/livros/novo", methods=["GET", "POST"])
def books_new():
    session = SessionLocal()
    usuarios = session.scalars(select(User).order_by(User.nome)).all()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        user_id = request.form.get("user_id")

        if titulo and user_id:
            session = SessionLocal()
            livro = session.scalar(select(Book).where(Book.titulo == titulo, Book.user_id == int(user_id)))
            if not livro:
                session.add(Book(titulo=titulo, user_id=int(user_id)))
                session.commit()
            return redirect(url_for("index"))

    return render_template("book_form.html", usuarios=usuarios)


if __name__ == "__main__":
    app.run(debug=True)
