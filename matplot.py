import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 10})
rotulos = ['18 a 27 anos', '28 a 39 anos', '40 a 55 anos', 'acima 55 anos']
valores = [40, 14, 17, 29]
c = ['#ddb9b2', '#c2c9cd', '#4a8ab7', '#525e75']
explode = (.1, 0, .1, 0)

plt.figure(figsize=(8, 8))

plt.pie(x=valores, labels=rotulos, autopct='%1.1f%%', colors=c, shadow=True, explode=explode)
plt.savefig('teste.png')
plt.show()
plt.close()

# plt.rcParams.update({'font.size': 10})
# rotulos = ['18 a 27 anos', '28 a 39 anos', '40 a 55 anos', 'acima 55 anos']
# valores = [dezoito_porc, vinteoito_porc, quarenta_porc, cinquenta_porc]
# c = ['#ddb9b2', '#c2c9cd', '#4a8ab7', '#525e75']
# explode = (.1, 0, .1, 0)
#
# plt.figure(figsize=(8, 8))
#
# plt.pie(x=valores, labels=rotulos, autopct='%1.1f%%', colors=c, shadow=True, explode=explode)
# plt.savefig('static/imagens/teste.png')
# plt.show()
# plt.close()
