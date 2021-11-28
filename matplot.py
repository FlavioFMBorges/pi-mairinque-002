import matplotlib.pyplot as plt

a = 15.56
b = 44.44
c = 31.11
d = 8.89

plt.rcParams.update({'font.size':10})
rotulos = ['18 a 27 anos', '28 a 39 anos', '40 a 55 anos', 'acima 55 anos']
valores = [a, b, c, d]
c = ['#ddb9b2', '#c2c9cd', '#4a8ab7', '#525e75']
explode = (.1, 0, .1, 0)

plt.figure(figsize=(8, 8))

plt.pie(x=valores, labels=rotulos, autopct='%1.1f%%', colors=c, shadow=True, explode=explode)
plt.savefig('static/imagens/teste_5.png')
plt.show()
plt.close()
