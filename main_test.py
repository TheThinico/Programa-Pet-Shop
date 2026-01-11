import banco_de_dados

# user_name = "thiago"
# pass_word = "mPKueWWlKg2MsWhk"
user_name = (input("NOME: "))
pass_word = (input("SENHA: "))

#Codigo pra linkar ao banco o usuario
data = banco_de_dados.conectar_banco(user_name, pass_word)

#database_connect.link_database(user_name, pass_word)
#database_connect.database_login()

