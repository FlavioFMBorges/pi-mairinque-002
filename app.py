import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import os
import datetime
from werkzeug.exceptions import abort

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
