from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import matplotlib.pyplot as plt
from init_db import get_db_connection
from constantes import paleta_cores, rotulos
from comandos_sql import query_selecionar_tipo_fraude, query_todos_participantes , query_inserir_post, query_selecionar_por_idade
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'anystringthatyoulike'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ranking')
def ranking():
    return render_template('ranking.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contate')
def contate():
    return render_template('contate.html')

@app.route('/formulario', methods=('GET', 'POST'))
def formulario():
    conexao_form = get_db_connection()
    cursor_form = conexao_form.cursor()
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
            cursor_form.execute(
                        query_inserir_post,
                        (nome, email, idade, tipo, opcao, valida, fraude))
            conexao_form.commit()

            if nome:
                flash(
                    'Muito obrigada por preencher nossa pesquisa. Com certeza você estará ajudando alguma pessoa em algum lugar do Brasil!')
    
            cursor_form.close()
            conexao_form.close()
            return redirect(url_for('formulario'))
    return render_template('formulario.html')

@app.route('/relatorio', methods=('GET', 'POST'))
def relatorio():
# variaveis filtradas do bd para substituir porcentagem na pagina relatório a cada envio do formulário para o bd
    conexao_rel = get_db_connection()
    cursor_rel = conexao_rel.cursor()

    cursor_rel.execute(query_todos_participantes)
    participa = cursor_rel.fetchone()['COUNT(*)']
    cursor_rel.execute(query_selecionar_por_idade + '18 AND 27')
    dezoito = cursor_rel.fetchone()['COUNT(*)']
    dezoito_porc = ((dezoito / participa) * 100)

    cursor_rel.execute(query_selecionar_por_idade + '28 AND 39')
    vinteoito = cursor_rel.fetchone()['COUNT(*)']
    vinteoito_porc = ((vinteoito / participa) * 100)

    cursor_rel.execute(query_selecionar_por_idade + '40 AND 55') 
    quarenta = cursor_rel.fetchone()['COUNT(*)']
    quarenta_porc = ((quarenta / participa) * 100)

    cursor_rel.execute(query_selecionar_por_idade +  '55 AND 120')
    cinquenta = cursor_rel.fetchone()['COUNT(*)']
    cinquenta_porc = ((cinquenta / participa) * 100)

# variáveis tiradas do bd para uso do if logo abaixo
    cursor_rel.execute(query_selecionar_tipo_fraude + "'op%'")
    tot_opcao = cursor_rel.fetchone()['COUNT(*)']

    cursor_rel.execute(query_selecionar_tipo_fraude + "'op2'")
    whats = cursor_rel.fetchone()['COUNT(*)']
    whats_porc = ((whats / tot_opcao) * 100)

    cursor_rel.execute(query_selecionar_tipo_fraude + "'op1'")
    pix = cursor_rel.fetchone()['COUNT(*)']
    pix_porc = ((whats / tot_opcao) * 100)

    cursor_rel.execute(query_selecionar_tipo_fraude + "'op3'")
    sitenet =  cursor_rel.fetchone()['COUNT(*)']
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
    valores = [dezoito_porc, vinteoito_porc, quarenta_porc, cinquenta_porc]
    explode = (.1, 0, .1, 0)

    plt.figure(figsize=(8, 8))

    plt.pie(x=valores, labels=rotulos, autopct='%1.1f%%', colors=paleta_cores, shadow=True, explode=explode)
    plt.savefig('static/imagens/diagrama-pizza.png')
    plt.show()
    plt.close()
# produz uma imagem do gráfico da home salvando na pasta a imagem nova a cada entrada no bd. Link para index.html
    plt.rcParams.update({'font.size': 10})
    valores = [dezoito_porc, vinteoito_porc, quarenta_porc, cinquenta_porc]
    explode = (.1, 0, .1, 0)

    plt.figure(figsize=(4, 2))

    plt.pie(x=valores, labels=rotulos, autopct='%1.1f%%', colors=paleta_cores, shadow=True, explode=explode)
    plt.savefig('static/imagens/grafico.png', transparent=True)
    plt.show()
    plt.close()

    cursor_rel.close()
    conexao_rel.close()

    return render_template('relatorio.html', COUNT=participa, dezoito=dezoito_porc, vinteoito=vinteoito_porc,
                           quarenta=quarenta_porc, cinquenta=cinquenta_porc, porcentagem_fraude=porcentagem_fraude, meio_fraude=meio_fraude, maior=maior)

if __name__ == '__main__':
    app.run(debug=True)