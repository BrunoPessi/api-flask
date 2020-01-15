from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1712@localhost/flaskapi"
db = SQLAlchemy(app)


class Aluno(db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    media = db.Column(db.Integer)

    def __init__(self, nome, media):
        self.nome = nome
        self.media = media


@app.route('/')
def index():
    alunos = Aluno.query.all()
    return render_template('index.html', alunos=alunos)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        aluno = Aluno(request.form['nome'], request.form['media'])
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("add.html")


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    aluno = Aluno.query.get(id)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.media = request.form['media']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("edit.html", aluno=aluno)


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    aluno = Aluno.query.get(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
