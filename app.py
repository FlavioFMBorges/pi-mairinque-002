from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import matplotlib.pyplot as plt
import pymysql
import pymysql.cursors

def get_db_connection():
    conn = pymysql.connect(
        host= 'database-2.c05d0e8qcds2.sa-east-1.rds.amazonaws.com',
        port = 3306,
        user ='admin',
        password ='projeto2',
        cursorclass=pymysql.cursors.DictCursor,
        db='sys'
        )
    return conn

# Conexão com banco de dados
def get_post(post_id):
    x = get_db_connection()
    with x:
        with x.cursor() as conn:
            post = conn.query('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
            conn.close()
            if post is None:
                abort(404)
            return post
    x.commit()



app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/index')
@app.route('/')
def index():
    x = get_db_connection()
    with x:
        with x.cursor() as conn:
            conn = get_db_connection()
            print(conn)
            posts = conn.query('SELECT * FROM posts')
            conn.close()
            return render_template('index.html', posts=posts)





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

        if not nome:
            flash('Insira o nome completo!')
        else:
            x = get_db_connection()
            with x:
                with x.cursor() as connx:
                    connx.execute(
                        'INSERT INTO posts ( nome, email, idade, tipo, opcao, valida, fraude) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (nome, email, idade, tipo, opcao, valida, fraude))
                x.commit()
            if nome:
                flash(
                    'Muito obrigada por preencher nossa pesquisa. Concerteza você estará ajudando alguma pessoa em algum lugar do Brasil!')
            return redirect(url_for('formulario'))
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


        if not nome:
            flash('Insira o nome!')
        else:
            conn = get_db_connection()
            conn.query(
                'UPDATE posts SET nome = ?, "email" = ?, "idade" = ?, "tipo" = ?, "opcao" = ?, "valida" = ?, "fraude" = ?, "descricao" = ?  '
                ' WHERE id = ?',
                (nome, email, idade, tipo, opcao, valida, fraude, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.query('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['nome']))
    return redirect(url_for('index'))


@app.route('/ranking')
def ranking():
    return render_template('ranking.html')


@app.route('/relatorio', methods=('GET', 'POST'))
def relatorio():
    conn = get_db_connection()
# variaveis filtradas do bd para substituir porcentagem na pagina relatório a cada envio do formulário para o bd
    participa = conn.query('SELECT COUNT(*) FROM posts') or 0
    dezoito = conn.query('SELECT COUNT(*) FROM posts WHERE idade BETWEEN 18 AND 27') or 0
    dezoito_porc = ((dezoito / participa) * 100)
    vinteoito = conn.query('SELECT COUNT(*) FROM posts WHERE idade BETWEEN 28 AND 39') or 0
    vinteoito_porc = ((vinteoito / participa) * 100)
    quarenta = conn.query('SELECT COUNT(*) FROM posts WHERE idade BETWEEN 40 AND 55"') or 0
    quarenta_porc = ((quarenta / participa) * 100)
    cinquenta = conn.query('SELECT COUNT(*) FROM posts WHERE idade > 55') or 0
    cinquenta_porc = ((cinquenta / participa) * 100)
# variáveis tiradas do bd para uso do if logo abaixo
    tot_opcao = conn.query('SELECT COUNT(*) FROM posts WHERE opcao LIKE "op%"') or 0
    whats = conn.query('SELECT COUNT(*) FROM posts WHERE opcao LIKE "op2"') or 0
    whats_porc = ((whats / tot_opcao) * 100)

    pix = conn.query('SELECT COUNT(*) FROM posts WHERE opcao LIKE "op1"') or 0
    pix_porc = ((whats / tot_opcao) * 100)

    sitenet = conn.query('SELECT COUNT(*) FROM posts WHERE opcao LIKE "op3"') or 0
    sitenet_porc = ((whats / tot_opcao) * 100)
# variavel maior pega o maior valor depois compara para substituir texto e porcentagem na pagina relatório
    maior = max(pix, whats, sitenet)
    if maior == pix:
        meio_fraude = ('Pix')
        porcentagem_fraude = pix_porc
    elif maior == whats:
        meio_fraude = ('mensagens pelo aplicativo WhatsApp')
        porcentagem_fraude = whats_porc
    else:
        meio_fraude = ('um site da internet')
        porcentagem_fraude = sitenet_porc
# produz uma imagem do gráfico da relatório salvando na pasta a imagem nova a cada entrada no bd. Link para relatório
    plt.rcParams.update({'font.size': 10})
    rotulos = ['18 a 27 anos', '28 a 39 anos', '40 a 55 anos', 'acima 55 anos']
    valores = [dezoito_porc, vinteoito_porc, quarenta_porc, cinquenta_porc]
    c = ['#ddb9b2', '#f41100', '#4a8ab7', '#fcec00']
    explode = (.1, 0, .1, 0)

    plt.figure(figsize=(8, 8))

    plt.pie(x=valores, labels=rotulos, autopct='%1.1f%%', colors=c, shadow=True, explode=explode)
    plt.savefig('static/imagens/diagrama-pizza.png')
    plt.show()
    plt.close()
# produz uma imagem do gráfico da home salvando na pasta a imagem nova a cada entrada no bd. Link para index.html
    plt.rcParams.update({'font.size': 10})
    rotulos = ['18 a 27 anos', '28 a 39 anos', '40 a 55 anos', 'acima 55 anos']
    valores = [dezoito_porc, vinteoito_porc, quarenta_porc, cinquenta_porc]
    c = ['#ddb9b2', '#f41100', '#4a8ab7', '#fcec00']
    explode = (.1, 0, .1, 0)

    plt.figure(figsize=(4, 2))

    plt.pie(x=valores, labels=rotulos, autopct='%1.1f%%', colors=c, shadow=True, explode=explode)
    plt.savefig('static/imagens/grafico.png', transparent=True)
    plt.show()
    plt.close()

    conn.commit()
    conn.close()
    return render_template('relatorio.html', COUNT=participa, dezoito=dezoito_porc, vinteoito=vinteoito_porc,
                           quarenta=quarenta_porc, cinquenta=cinquenta_porc, porcentagem_fraude=porcentagem_fraude, meio_fraude=meio_fraude, maior=maior)


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/contate')
def contate():
    return render_template('contate.html')

if __name__ == '__main__':
    app.run(debug=True)