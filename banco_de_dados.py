from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pymongo.errors import DuplicateKeyError

#    ---------------------------
#   Classe de link pro banco

class db:
    """
        Classe de conecção com banco de dados.
        Use ele para chamar funções que exijam pesquisa com o banco de dados.
    """
    def __init__(self):
        self.client = None
        self.conectar_banco()

    #caso não tenha dados de login
    @staticmethod
    def dados_login_banco():
        username = (input("NOME: "))
        password = (input("SENHA: "))
        return username, password

    #faz o login no bando de dados
    def conectar_banco(self):
        print("Conectando ao banco... ")

        x = self.dados_login_banco()
        user_name = x[0]
        pass_word = x[1]

        uri = f"mongodb+srv://{user_name}:{pass_word}@cluster0.164lard.mongodb.net/?appName=Cluster0"

        # Create a new client and connect to the server
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        try:
            self.client.admin.command('ping')
            print("Ping enviado. Conecção com MongoDB feita com Sucesso!")

        except Exception as e:
            print(e)


# ================= SALVAR NO BANCO =================

def salvar_usuario_banco(cliente, dicionario):
    """
    Salva um usuario no banco de dados.
    Banco e Tabela pré selecionado.
    Da erro se cadastrar CPF existente no sistema.

    :param cliente: Link com o banco de dados
    :param dicionario: Dicionario com dados do usuário.
    """

    mydb = cliente["banco"]
    mycol = mydb["cadastro_usuario"]

    mycol.create_index("cpf", unique=True)

    try:
        x = mycol.insert_one(dicionario)
        #print(x)
        print(dicionario)
        print("Dados Cadastrados com Sucesso")
    except DuplicateKeyError as e:
        print(e)
        print("ERRO: CPF ja cadastrado")
    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)

def salvar_animal_banco(cliente, dicionario):
    """
    Salva um animal no banco de dados.
    Banco e Tabela pré selecionado.
    Obrigatório identificar seu tutor e respectivo CPF.

    :param cliente: Link com o banco de dados
    :param dicionario: Dicionario com dados do animal.
    :param dono: Dicionario do tutor do animal (somente o CPF é necessário)
    """

    mydb = cliente["banco"]
    mycol = mydb["cadastro_animal"]
    # dicionario.update(
    #     {"tutor_cpf": dono["cpf"]})

    try:
        x = mycol.insert_one(dicionario)
        #print(x)
        print(x.inserted_id)
        print("Dados Cadastrados com Sucesso")
    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)

def salvar_consulta(cliente, dicionario, dono, animal):
    """
    Salva um animal no banco de dados.
    Banco e Tabela pré selecionado.
    Obrigatório identificar seu tutor e respectivo CPF.

    :param cliente: Link com o banco de dados.
    :param dono: Dicionario do tutor do animal.
    :param animal: Dicionario com dados do animal.
    """
    mydb = cliente["banco"]
    mycol = mydb["cadastro_usuario"]

    dicionario.update(
        {"tutor_cpf": dono["cpf"], "animal_nome": animal["nome"]}
    )

    try:
        x = mycol.insert_one(dicionario)
        #print(x)
        print(x.inserted_id)
        print("Dados Cadastrados com Sucesso")
    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)
    pass


# ================= PESQUISAR NO BANCO =================

def pesquisar_usuario(cliente, informacao, return_info = False):
    """
        Busoca dados de um Usuario. Pode retornar os dados em JSON/Dicionário.

        :param cliente: Link com o banco de dados
        :param informacao: Informação que deseja localizar alguém (por padrão é o CPF)
        :param return_info: Se True ele retorna o usuário
        :return: Resultado da soma
    """

    mydb = cliente["banco"]
    mycol = mydb["cadastro_usuario"]

    for x in mycol.find({"cpf": informacao}):
        print (x)
        if x != None and return_info == True:
            return x
    print("Usuario Não Encontrado")

def pesquisar_pet(cliente, dono, informacao):
    """
        Busca dados de um animal. Pode retornar uma lista de dados, em JSON/Dicionário.

        :param cliente: Link com o banco de dados.
        :param informacao: Informação que deseja localizar alguém (por padrão é o NOME do animal).
        :param return_user: Se True ele retorna o usuário.
        :return: Retorna uma Lista de Dicionários de animais encontrado.
    """
    mydb = cliente["banco"]
    mycol = mydb["cadastro_animal"]

    for x in mycol.find({"cpf": informacao}):
        print (x["nome"])
        return x

def pesquisar_consulta(cliente, informacao, return_info = False):
    """
        Busca dados de um usuario. Pode retornar os dados em JSON/Dicionário se "return_info" for True.

        :param cliente: Link com o banco de dados.
        :param informacao: Informação que deseja localizar alguém (por padrão é o CPF).
        :param return_info: Se True, a função retornará o usuário.
        :return: Resultado da soma
    """

    mydb = cliente["banco"]
    mycol = mydb["cadastro_consulta"]

    for x in mycol.find({"cpf": informacao}):
        print (x)
        if x != None and return_info == True:
            return x
    print("Usuario Não Encontrado")


# ================= CODIGO LEGADO =================

# def pesquisar_dados_banco(cliente, tabela, informacao,  chave = None):
#     #(pode haver falhas se houver informações semelhantes). Retorna JSON/Dicionário
#
#     mydb = cliente["banco"]
#     mycol = mydb[tabela]
#
#     for x in mycol.find({chave: informacao}):
#         print (x)
#
# # salva informação no bando de dados. Precisa inserir QUAL lugar do banco (tabela) deseja colocar
# def salvar_dados_banco(cliente, tabela, dicionario):
#     mydb = cliente["banco"]
#     mycol = mydb[tabela]
#
#     try:
#         x = mycol.insert_one(dicionario)
#         print(x)
#         print(x.inserted_id)
#         print("Dados Cadastrados com Sucesso")
#
#     except Exception as e:
#         print("ERRO: dados não foram cadastrados")
#         print (e)

# def database_login(database_username, database_password):
#     print("Logando no Banco: ", end="")
#     try:
#         uri = f"mongodb+srv://{database_username}:{database_password}@cluster0.164lard.mongodb.net/?appName=Cluster0"
#
#         # Create a new client and connect to the server
#         client = MongoClient(uri, server_api=ServerApi('1'))
#
#         # Send a ping to confirm a successful connection
#         try:
#             client.admin.command('ping')
#             print("Pinged your deployment. You successfully connected to MongoDB!")
#         except Exception as e:
#             print("Não fui 1")
#             print(e)
#     except Exception as e:
#         print("Não fui 2")
#         print(e)
#
# #selecionando banco de dados e insere os dados na tabela
# def save_database_datas(client, dictionary_data):
#     mydb = client["banco"]
#     mycol = mydb["cadastro"]
#
#     # dicionario  = [
#     #         {"nome": "Andre", "idade" : "89"},
#     #         {"nome": "Maria", "idade" : "38"}]
#
#     try:
#         x = mycol.insert_many(dictionary_data)
#         print(x)
#         print(x.inserted_ids)
#     except:
#         print("ERRO: dados não foram cadastrados")
