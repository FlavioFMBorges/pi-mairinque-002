import sqlite3
from flask import Flask, render_template
# request, url_for, flash, redirect
# import os
# import datetime
# from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


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


@app.route('/ranking')
def ranking():
    return render_template('ranking.html')


@app.route('/formulario')
def formulario():
    return render_template('formulario.html')


@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/contate')
def contate():
    return render_template('contate.html')