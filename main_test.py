import banco_de_dados

#user_name = (input("NOME: "))
#pass_word = (input("SENHA: "))

#Codigo pra linkar ao banco o usuario

data = banco_de_dados.db()
link = data.client

pessoa = {
    "nome": "joao",
    "telefone": "00922224444",
    "email": "joaozinho@j.com",
    "cpf": "66677788822"
}

cao =  {
    "nome": "pongo",
    "tipo": "gato",
    "raca": "bombai",
    "idade": 7,
    "tutor_cpf": pessoa["cpf"]
}

banco_de_dados.salvar_usuario_banco(link,pessoa)
banco_de_dados.salvar_animal_banco(link, cao)

#database_connect.link_database(user_name, pass_word)
#database_connect.database_login()



