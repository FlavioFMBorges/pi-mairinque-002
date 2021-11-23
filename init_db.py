import sqlite3

connection = sqlite3.connect('database.db')

with open('schemas.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO posts (nome, email, idade, tipo, opcao, valida, fraude, descricao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    ('First Post', 'Content for the first post', '13', 'S', 'OP1', 'S', 'S', 'AMIGO')
    )

cur.execute(
    "INSERT INTO posts (nome, email, idade, tipo, opcao, valida, fraude, descricao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    ('Second Post', 'Content for the second post', '16', 'S', 'OP2', 'S', 'S', 'MAE')
    )

connection.commit()
connection.close()
