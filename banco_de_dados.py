from asyncio.windows_events import NULL

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#caso não tenha dados de login
def dados_login_banco():
    username = (input("NOME: "))
    password = (input("SENHA: "))
    return username, password

#faz o login no bando de dados
def conectar_banco(user_name = None, pass_word = None):
    print("Conectando ao banco: ", end="")

    if user_name == None or pass_word == None:
        x = dados_login_banco()
        user_name = x[0]
        pass_word = x[1]

    uri = f"mongodb+srv://{user_name}:{pass_word}@cluster0.164lard.mongodb.net/?appName=Cluster0"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)

# salva informação no bando de dados
# precisa inserir QUAL lugar do banco (tabela) deseja colocar
def salvar_dados_banco(cliente, tabela, dicionario):
    mydb = cliente["banco"]
    mycol = mydb[tabela]

    try:
        x = mycol.insert(dicionario)
        print(x)
        print(x.inserted_ids)
        print("Dados Cadastrados com Sucesso")
    except:
        print("ERRO: dados não foram cadastrados")

# faz pesquisa no banco de dados (pode haver falhas se houver informações semelhantes)
# retorna JSON/Dicionário
def pesquisar_dados_banco(cliente, tabela, informacao, chave = None):
    mydb = cliente["banco"]
    mycol = mydb[tabela]

    for x in mycol.find({chave: informacao}):
        print (x)

# faz pesquisa de USUARIO no banco
# retorna uma lista de JSON/Dicionário
def pesquisar_usuario(cliente, informacao, chave = None):
    mydb = cliente["banco"]
    mycol = mydb["usuarios"]

    list = []
    for x in mycol.find({chave: informacao}):
        list.append(x)
    return list

#    ---------------------------
# CODIGO LEGADO - não utilizar

#faz o login no bando de dados
def database_login(database_username, database_password):
    print("Logando no Banco: ", end="")
    try:
        uri = f"mongodb+srv://{database_username}:{database_password}@cluster0.164lard.mongodb.net/?appName=Cluster0"

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print("Não fui 1")
            print(e)
    except Exception as e:
        print("Não fui 2")
        print(e)

#selecionando banco de dados e insere os dados na tabela
def save_database_datas(client, dictionary_data):
    mydb = client["banco"]
    mycol = mydb["cadastro"]

    # dicionario  = [
    #         {"nome": "Andre", "idade" : "89"},
    #         {"nome": "Maria", "idade" : "38"}]

    try:
        x = mycol.insert_many(dictionary_data)
        print(x)
        print(x.inserted_ids)
    except:
        print("ERRO: dados não foram cadastrados")

