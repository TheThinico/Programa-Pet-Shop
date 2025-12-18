import database_connect

# user_name = "thiago"
# pass_word = "mPKueWWlKg2MsWhk"
user_name = (input("NOME: "))
pass_word = (input("SENHA: "))
database_connect.set_login_datas(user_name, pass_word)
database_connect.database_login()