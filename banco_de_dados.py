from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pymongo.errors import DuplicateKeyError

#    ---------------------------
#   Classe de link pro banco

class Db_Client:
    link = None
    database = None

    def __init__(self):
        self.conectar_banco()

    def conectar_banco(self):
        print("Conectando ao banco... ")

        user_name, pass_word = self.dados_login_banco()

        uri = f"mongodb+srv://{user_name}:{pass_word}@cluster0.164lard.mongodb.net/"
        self.link = MongoClient(uri, server_api=ServerApi('1'))

        self.database = self.link["banco"]  # ✅ banco fixo

        self.link.admin.command('ping')
        print("Conectado com sucesso!")


    #caso não tenha dados de login
    @staticmethod
    def dados_login_banco():
        username = (input("NOME: "))
        password = (input("SENHA: "))
        return username, password

    # #faz o login no bando de dados
    # def conectar_banco(self):
    #     print("Conectando ao banco... ")
    #
    #     x = self.dados_login_banco()
    #     user_name = x[0]
    #     pass_word = x[1]
    #
    #     uri = f"mongodb+srv://{user_name}:{pass_word}@cluster0.164lard.mongodb.net/?appName=Cluster0"
    #
    #     # Create a new client and connect to the server
    #     self.client = MongoClient(uri, server_api=ServerApi('1'))
    #     try:
    #         self.client.admin.command('ping')
    #         print("Ping enviado. Conecção com MongoDB feita com Sucesso!")
    #
    #     except Exception as e:
    #         print(e)

# ================= CLIENTE / ANIMAL =================

#   ----- Salvar -----
def salvar_tutor(link, tutor_dados):
    """
    Salva um usuario no banco de dados.
    Banco e Tabela pré selecionado.
    Da erro se cadastrar CPF existente no sistema.

    :param link: Link com o banco de dados
    :param tutor_dados: Dicionario com dados do usuário.
    """

    db = link["banco"]
    colecao = db["cadastro_clientes"]

    colecao.create_index("cpf", unique=True)

    try:
        x = colecao.insert_one(tutor_dados)
        #print(x)
        print(tutor_dados)
        print("Dados Cadastrados com Sucesso")
    except DuplicateKeyError as e:
        print(e)
        print("ERRO: CPF ja cadastrado")
    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)

def salvar_animal(link, animal_dados):
    """
    Salva um animal no banco de dados.
    Banco e Tabela pré selecionado.
    Obrigatório identificar seu tutor e respectivo CPF.

    :param link: Link com o banco de dados
    :param animal_dados: Dicionario com dados do animal.
    """

    db = link["banco"]
    colecao = db["cadastro_animal"]
    # dicionario.update(
    #     {"tutor_cpf": dono["cpf"]})

    try:
        x = colecao.insert_one(animal_dados)
        #print(x)
        print(x.inserted_id)
        print("Dados Cadastrados com Sucesso")
    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)

#   ----- Buscar -----
def buscar_tutor_por_cpf(link, cpf):
    db = link["banco"]
    colecao = db["clientes"]

    return colecao.find_one({"cpf": cpf}, {"_id": 0})

def buscar_tutor_por_nome(link, nome):
    """
    Busca um cliente pelo nome no banco de dados.
    Retorna o dicionário do cliente ou None se não encontrado.
    """
    db = link["banco"]
    colecao = db["clientes"]

    resultado = colecao.find_one({"nome": {"$regex": f"^{nome}$", "$options": "i"}})  # Case-insensitive
    return resultado

def buscar_animal_por_nome(link, nome_pet, tutor_cpf):
    """
    Busca um animal pelo nome do pet e CPF do tutor.

    :param link: objeto de conexão com o MongoDB (banco.client)
    :param nome_pet: nome do animal (string)
    :param tutor_cpf: CPF do tutor (string)
    :return: dicionário com dados do animal ou None se não encontrado
    """
    colecao = link["banco"]["cadastro_animal"]

    try:
        animal = colecao.find_one({
            "nome": {"$regex": f"^{nome_pet}$", "$options": "i"},
            "tutor_cpf": tutor_cpf
        })
        if animal:
            return animal
        else:
            return None
    except Exception as e:
        print("❌ Erro ao buscar animal:", e)
        return None

def buscar_animais_tutor(link, tutor):
    """
        Mostra uma Lista de animais de um tutor. Pode retornar uma lista de dados, em JSON/Dicionário.

        :param link: Link com o banco de dados.
        :param tutor: Informação que deseja localizar alguém (por padrão é o NOME do animal).
    """
    db = link["banco"]
    colecao = db["cadastro_animal"]

    lista = []

    for x in colecao.find({"tutor_cpf": tutor["cpf"]}):
        #print (x["nome"])
        lista.append(x)
    return lista

#   ----- Atualizar/Excluir -----
def atualizar_tutor(link, cpf, novos_dados):
    db = link["banco"]
    colecao = db["clientes"]

    return colecao.update_one(
        {"cpf": cpf},
        {"$set": novos_dados}
    )

def excluir_tutor(link , cpf):
    db = link["banco"]
    colecao = db["clientes"]
    return colecao.delete_one({"cpf": cpf})

# ================= FUNCIONARIOS =================

def salvar_funcionario(link, funcionario):
    db = link["banco"]
    colecao = db["funcionarios"]

    colecao.create_index("cpf", unique=True)
    colecao.insert_one(funcionario)

#   ----- Buscar -----
def lista_funcionarios(link):
    db = link["banco"]
    colecao = db["funcionarios"]

    return list(colecao.find({}, {"_id": 0}))

def buscar_funcionario(link, cpf):
    db = link["banco"]
    colecao = db["funcionarios"]

    return colecao.find_one({"cpf": cpf}, {"_id": 0})
    return colecao.find_one({"cpf": cpf})

#   ----- Atualizar/Excluir -----
def atualizar_funcionario(link, cpf, novos_dados):
    db = link["banco"]
    colecao = db["funcionarios"]
    return colecao.update_one(
        {"cpf": cpf},
        {"$set": novos_dados}
    )

def excluir_funcionario(link, cpf):
    db = link["banco"]
    colecao = db["funcionarios"]

    return colecao.delete_one({"cpf": cpf})

# ================= BANHO E TOSA / CLINICO =================

def salvar_agendamento_banho_tosa(link, agendamento):
    """
    Salva um agendamento de banho e tosa no banco.
    """
    db = link["banco"]
    colecao = db["agendamento_banho_tosa"]

    try:
        colecao.insert_one(agendamento)
        print("✅ Agendamento de banho e tosa cadastrado com sucesso!\n")
    except Exception as e:
        print("❌ Erro ao salvar o agendamento: ", e)

def salvar_agendamento_clinico(link, agendamento):
    """
    Salva um agendamento de banho e tosa no banco.
    """
    db = link["banco"]
    colecao = db["agendamento_clinico"]

    try:
        colecao.insert_one(agendamento)
        print("✅ Agendamento de banho e tosa cadastrado com sucesso!\n")
    except Exception as e:
        print("❌ Erro ao salvar o agendamento: ", e)

#   ----- Buscar -----
def pesquisar_consulta(link, informacao, return_info = False):
    """
        Busca dados de um usuario. Pode retornar os dados em JSON/Dicionário se "return_info" for True.

        :param link: Link com o banco de dados.
        :param informacao: Informação que deseja localizar alguém (por padrão é o CPF).
        :param return_info: Se True, a função retornará o usuário.
        :return: Resultado da soma
    """

    db = link["banco"]
    colecao = db["cadastro_consulta"]

    for x in colecao.find({"cpf": informacao}):
        print (x)
        if x != None and return_info == True:
            return x
    print("Usuario Não Encontrado")

def pesquisar_banho_e_tosa_por_nome(link, nome):
    colecao = link["agendamento_banho_tosa"]

    return colecao.find_one({"cliente": nome})

def listar_clientes(client):
    db = client["banco"]
    colecao = db["clientes"]

    return list(colecao.find({}, {"_id": 0}))

# ================= LEGADO =================

# def salvar_clientes_banco(link, cliente):
#     db = link["banco"]
#     colecao = db["clientes"]
#
#     colecao.create_index("cpf", unique=True)
#     colecao.insert_one(cliente)

#def salvar_agendamento_animal(link, dicionario, dono, animal):
#
#     db = link["banco"]
#     colecao = db["agendamento_clinico_pet"]
#
#     dicionario.update(
#         {"tutor_cpf": dono["cpf"], "animal_nome": animal["nome"]}
#     )
#
#     try:
#         x = colecao.insert_one(dicionario)
#         #print(x)
#         print(x.inserted_id)
#         print("Dados Cadastrados com Sucesso")
#     except Exception as e:
#         print("ERRO: dados não foram cadastrados")
#         print (e)
#     pass