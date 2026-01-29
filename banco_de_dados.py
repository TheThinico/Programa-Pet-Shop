from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pymongo.errors import DuplicateKeyError
import modelos

#    ---------------------------
#   Classe de link pro banco

class Db_Client:

    database = None

    def __init__(self):
        self.conectar_banco()

    def conectar_banco(self):
        print("Conectando ao banco... ")

        user_name, pass_word = self.dados_login_banco()

        uri = f"mongodb+srv://{user_name}:{pass_word}@cluster0.164lard.mongodb.net/"
        link = MongoClient(uri, server_api=ServerApi('1'))

        self.database = link["banco"]  # ✅ banco fixo

        link.admin.command('ping')
        print("Conectado com sucesso!")


    #caso não tenha dados de login
    @staticmethod
    def dados_login_banco():
        username = (input("NOME: "))
        password = (input("SENHA: "))
        return username, password

# ================= CLIENTE / ANIMAL =================

#   ----- Salvar -----
def salvar_tutor(db, tutor_dados : modelos.Tutor):
    """
    Salva um usuario no banco de dados.
    Banco e Tabela pré selecionado.
    Da erro se cadastrar CPF existente no sistema.

    :param db: Link com o banco de dados
    :param tutor_dados: Dicionario com dados do usuário.
    """
    #db = link["banco"]
    colecao = db["cadastro_clientes"]

    #colecao.create_index("cpf", unique=True)
    try:
        x = colecao.insert_one(tutor_dados.to_dict())
        print("✅ Dados Cadastrados com Sucesso")
    except DuplicateKeyError as e:
        print(e)
        print("ERRO: CPF ja cadastrado")
    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)

def salvar_animal(db, animal_dados : modelos.Animal):
    """
    Salva um animal no banco de dados.
    Banco e Tabela pré selecionados.

    :param db: Link com o banco de dados
    :param animal_dados: Dicionario com dados do animal.
    """
    #db = link["banco"]
    colecao = db["cadastro_animal"]
    try:
        x = colecao.insert_one(animal_dados.to_dict())
        print("✅ Dados Cadastrados com Sucesso")
    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)

#   ----- Buscar -----
def buscar_tutor_por_cpf(db, cpf):
    """
    Busca um cliente pelo CPF no banco de dados.
    Retorna o dicionário do cliente ou None se não encontrado.
    """
    #db = link["banco"]
    colecao = db["cadastro_clientes"]

    resultado = modelos.Tutor()
    resultado.set_dict(colecao.find_one({"cpf": cpf}, {"_id": 0}))
    if resultado.nome == "":
        return None
    else:
        return resultado

def buscar_tutor_por_nome(db, nome):
    """
    Busca um cliente pelo nome no banco de dados.
    Retorna o dicionário do cliente ou None se não encontrado.
    """
    #db = link["banco"]
    colecao = db["cadastro_clientes"]

    resultado = modelos.Tutor()
    resultado.set_dict(colecao.find_one({"nome": {"$regex": f"^{nome}$", "$options": "i"}}))  # Case-insensitive

    if resultado.nome == "":
        return None
    else:
        return resultado

def buscar_animal_por_nome(db, nome_pet, tutor_cpf):
    """
    Busca um animal pelo nome do pet e CPF do tutor.

    :param db: objeto de conexão com o MongoDB (banco.client)
    :param nome_pet: nome do animal (string)
    :param tutor_cpf: CPF do tutor (string)
    :return: dicionário com dados do animal ou None se não encontrado
    """
    colecao = db["cadastro_animal"]

    resultado = modelos.Animal()
    try:
        resultado.set_dict(colecao.find_one({"nome": {"$regex": f"^{nome_pet}$", "$options": "i"},"tutor_cpf": tutor_cpf})
        )
        if resultado.nome == "":
            return None
        else:
            return resultado
    except Exception as e:
        print("❌ Erro ao buscar animal:", e)
        return None

def buscar_animais_tutor(db, tutor_cpf):
    """
        Mostra uma Lista de animais de um tutor. Pode retornar uma lista de dados, em JSON/Dicionário.

        :param db: Link com o banco de dados.
        :param tutor_cpf: dado usado para pesquisar no banco.
        :return: Lista de dicionarios.
    """
    #db = link["banco"]
    colecao = db["cadastro_animal"]

    lista = []

    for x in colecao.find({"tutor_cpf": tutor_cpf}):
        animal = modelos.Animal()
        lista.append(animal.set_dict(x))
    return lista

# ================= FUNCIONARIOS =================

def salvar_funcionario(db, funcionario_dados : modelos.Funcionario):
    #db = link["banco"]
    colecao = db["cadastro_funcionarios"]
    colecao.create_index("cpf", unique=True)

    try:
        x = colecao.insert_one(funcionario_dados.to_dict())
        # print(x)
        # print(funcionario_dados)
        print("✅ Dados Cadastrados com Sucesso")
    except DuplicateKeyError as e:
        print(e)
        print("ERRO: CPF ja cadastrado")
    except Exception as e:
        print("ERRO: dados não foram cadastrados")
        print (e)

#   ----- Buscar -----
def lista_funcionarios(db):
    #db = link["banco"]
    colecao = db["cadastro_funcionarios"]

    return list(colecao.find({}, {"_id": 0}))

def buscar_funcionario(db, cpf):
    #db = link["banco"]
    colecao = db["cadastro_funcionarios"]

    return colecao.find_one({"cpf": cpf}, {"_id": 0})

#   ----- Atualizar/Excluir -----
def atualizar_funcionario(db, cpf, novos_dados):
    #db = link["banco"]
    colecao = db["cadastro_funcionarios"]
    return colecao.update_one(
        {"cpf": cpf},
        {"$set": novos_dados}
    )

# ================= SERVIÇO =================

def salvar_agendamento_servico(db, agendamento):
    """
    Salva um agendamento de banho e tosa no banco
    \n 1) banho e tosa | 2) clinico
    """
    #db = link["banco"]
    colecao = db["agendamento_servico"]

    try:
        colecao.insert_one(agendamento)
    except Exception as e:
        raise ("❌ Erro ao salvar o agendamento: ", e)

#   ----- Buscar -----
def pesquisar_consulta(db, informacao, return_info = False):
    """
        Busca dados de um usuario. Pode retornar os dados em JSON/Dicionário se "return_info" for True.

        :param db: Link com o banco de dados.
        :param informacao: Informação que deseja localizar alguém (por padrão é o CPF).
        :param return_info: Se True, a função retornará o usuário.
        :return: Resultado da soma
    """

    #db = link["banco"]
    colecao = db["agendamento_servico"]

    pesquisa = []

    for x in colecao.find({"cpf": informacao}):
        pesquisa.append(x)
    if pesquisa != None and return_info == True:
        return pesquisa
    else:
        print("Usuario Não Encontrado")
        return None

def listar_clientes(db):
    colecao = db["cadastro_clientes"]

    return list(colecao.find({}, {"_id": 0}))

# ================= LEGADO =================

# def excluir_funcionario(db, cpf):
#     #db = link["banco"]
#     colecao = db["cadastro_funcionarios"]
#
#     return colecao.delete_one({"cpf": cpf})

# def pesquisar_banho_e_tosa_por_nome(db, nome):
#     colecao = db["agendamento_banho_tosa"]
#
#     return colecao.find_one({"cliente": nome})

# def salvar_agendamento_banho_tosa(db, agendamento):
#     """
#     Salva um agendamento de banho e tosa no banco.
#     """
#     #db = link["banco"]
#     colecao = db["agendamento_banho_tosa"]
#
#     try:
#         colecao.insert_one(agendamento)
#         print("✅ Agendamento de banho e tosa cadastrado com sucesso!\n")
#     except Exception as e:
#         print("❌ Erro ao salvar o agendamento: ", e)
#
# def salvar_agendamento_clinico(db, agendamento):
#     """
#     Salva um agendamento de banho e tosa no banco.
#     """
#     #db = link["banco"]
#     colecao = db["agendamento_clinico"]
#
#     try:
#         colecao.insert_one(agendamento)
#         print("✅ Agendamento de banho e tosa cadastrado com sucesso!\n")
#     except Exception as e:
#         print("❌ Erro ao salvar o agendamento: ", e)


#   ----- Atualizar/Excluir -----
# def atualizar_tutor(link, cpf, novos_dados):
#     db = link["banco"]
#     colecao = db["cadastro_clientes"]
#
#     return colecao.update_one(
#         {"cpf": cpf},
#         {"$set": novos_dados}
#     )

# def excluir_tutor(db , cpf):
#     #db = link["banco"]
#     colecao = db["clientes"]
#
#     return colecao.delete_one({"cpf": cpf})

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