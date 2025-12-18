from http.cookiejar import user_domain_match

import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

database_username = ""
database_password = ""

# dados de Log-in
def set_login_datas(user_name, pass_word):
    try:
        database_username = user_name
        database_password = pass_word

        print("Dados gravados com sucesso")
    except:
        print("ERRO: dados não gravados")

#faz o login no bando de dados
def database_login():
    try:
        uri = f"mongodb+srv://{database_username}:{database_password}@cluster0.164lard.mongodb.net/?appName=Cluster0"

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)

#selecionando banco de dados e insere os dados na tabela
def set_database_datas(dictionary_data):
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

