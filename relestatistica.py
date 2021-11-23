import pandas as pd
import matplotlib.pyplot as plt



"""Leitura do arquivo csv da pesquisa"""


df = pd.read_csv('pesquisapi.csv')


""" Criar um diagrama de pizza para a coluna Idade) """


qtde = df['Qtde']

total = df['Part']

perc = (qtde / total) * 100

fig1, ax1 = plt.subplots(figsize=(8,8)) 

labels = '18 a 27 anos','28 a 39 anos','40 a 55 anos','acima 55 anos'
c =  ['#ddb9b2', '#c2c9cd', '#4a8ab7', '#525e75']
explode = (.1, 0, .1, 0) # Separa uma das fatias de acordo com indice e
# o valor dado(.1)


ax1.pie(perc, labels=labels,  autopct='%1.1f%%', colors=c,
        shadow=True, explode=explode)
plt.savefig('static/img/diagrama-pizza.png') 
plt.close()