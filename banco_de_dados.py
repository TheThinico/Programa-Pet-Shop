from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pymongo.errors import DuplicateKeyError

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
        print("Ping enviado. Conecção com MongoDB feita com Sucesso!")
        return client

    except Exception as e:
        print(e)

#    ---------------------------


# cadastra um USUARIO no banco de dados.
def salvar_usuario_banco(cliente, dicionario):
    # Banco e Tabela pré selecionado. Da erro se cadastrar CPF existente.

    mydb = cliente["banco"]
    mycol = mydb["cadastro"]

    mycol.create_index("cpf", unique=True)

    try:
        x = mycol.insert_one(dicionario)
        #print(x)
        print(x.inserted_id)
        print("Dados Cadastrados com Sucesso")
    except DuplicateKeyError:
        print("ERRO: CPF ja cadastrado")
    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)

# faz pesquisa no banco de dados
def pesquisar_dados_banco(cliente, tabela, informacao,  chave = None):
    #(pode haver falhas se houver informações semelhantes). Retorna JSON/Dicionário

    mydb = cliente["banco"]
    mycol = mydb[tabela]

    for x in mycol.find({chave: informacao}):
        print (x)

# faz pesquisa de USUARIO no banco.
def pesquisar_usuario(cliente, informacao):
    #Retorna uma lista de JSON/Dicionário

    mydb = cliente["banco"]
    mycol = mydb["cadastro"]

    for x in mycol.find({"cpf": informacao}):
        print (x)
        return x

def checar_usuario():
    pass


#    ---------------------------


# salva informação no bando de dados. Precisa inserir QUAL lugar do banco (tabela) deseja colocar
def salvar_dados_banco(cliente, tabela, dicionario):
    mydb = cliente["banco"]
    mycol = mydb[tabela]

    try:
        x = mycol.insert_one(dicionario)
        print(x)
        print(x.inserted_id)
        print("Dados Cadastrados com Sucesso")

    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)




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

