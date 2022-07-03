query_todos_participantes = 'SELECT COUNT(*) FROM posts'

query_selecionar_tipo_fraude ='SELECT COUNT(*) FROM posts WHERE opcao LIKE '
query_inserir_post = 'INSERT INTO posts ( nome, email, idade, tipo, opcao, valida, fraude) VALUES (%s, %s, %s, %s, %s, %s, %s)'
query_selecionar_por_idade = 'SELECT COUNT(*) FROM posts WHERE idade BETWEEN '