import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
# import os
# import datetime
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/index')
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/formulario', methods=('GET', 'POST'))
def formulario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        idade = request.form['idade']
        tipo = request.form['tipo']
        opcao = request.form['opcao']
        valida = request.form['valida']
        fraude = request.form['fraude']
        descricao = request.form['descricao']

        if not nome:
            flash('Insira o nome completo!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts ( nome, email, idade, tipo, opcao, valida, fraude, descricao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                         (nome, email, idade, tipo, opcao, valida, fraude, descricao))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('formulario.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        idade = request.form['idade']
        tipo = request.form['tipo']
        opcao = request.form['opcao']
        valida = request.form['valida']
        fraude = request.form['fraude']
        descricao = request.form['descricao']

        if not nome:
            flash('Insira o nome!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET nome = ?, "email" = ?, "idade" = ?, "tipo" = ?, "opcao" = ?, "valida" = ?, "fraude" = ?, "descricao" = ?  '
                         ' WHERE id = ?',
                         (nome, email, idade, tipo, opcao, valida, fraude, descricao, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['nome']))
    return redirect(url_for('index'))


@app.route('/ranking')
def ranking():
    return render_template('ranking.html')


# @app.route('/formulario')
# def formulario():
#    return render_template('formulario.html')


@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/contate')
def contate():
    return render_template('contate.html')
