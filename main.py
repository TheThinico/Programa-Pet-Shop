from datetime import datetime

import banco_de_dados

clientes = []
agendamentos_banho_tosa = []
agendamentos_clinicos = []

banco = banco_de_dados.db()

class usuario:
    def __init__(self,nome,telefone,email,cpf):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cpf = cpf

    def to_dict(self):
        return {
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "cpf": self.cpf,
        }

class animal:
    def __init__(self,nome,tipo,raca,idade,tutor_cpf):
        self.nome = nome
        self.tipo = tipo
        self.raca = raca
        self.idade = idade
        self.tutor_cpf = tutor_cpf

    def to_dict(self):
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "raca": self.raca,
            "idade": self.idade,
            "tutor_cpf": self.tutor_cpf,
        }

# ================= CLIENTES =================

# Opção 1
def cadastrar_cliente():
    print("\n👤 CADASTRO DE CLIENTE")
    novo_cliente = None
    choice = input("Possui cadastro? S ou N: ")

    if choice == "N" or choice == "n":
        print(f"Sua opção: {choice}")
        nome = input("Nome do cliente: ")
        telefone = input("Telefone: ")
        email = input("E-mail: ")
        cpf = validar_cpf(input("CPF: "))

        novo_cliente = usuario(nome,telefone,email,cpf)
        banco_de_dados.salvar_usuario_banco(banco.client, novo_cliente.to_dict())
    elif choice == "S" or choice == "s":
        novo_cliente = buscar_usuario(True)
        if novo_cliente == None:
            return
    else:
        print("Opção não encontrada")
        return

    print("registrar animal:")
    cadastrar_animal(novo_cliente)
    #clientes.append(cliente)
    #print("✅ Cliente cadastrado com sucesso!\n")

def cadastrar_animal(tutor):
    print("\n👤 CADASTRO DE ANIMAL")

    nome = input("Nome do animal: ")
    tipo = input("tipo de animal: ")
    idade = input("idade: ")
    raca = input("raça: ")
    tutor_cpf = tutor.cpf

    novo_animal = animal(nome,tipo,raca,idade,tutor_cpf)

    banco_de_dados.salvar_animal_banco(banco.client,novo_animal)

    # clientes.append(novo_animal)
    # print("✅ Cliente cadastrado com sucesso!\n")

def validar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")
    return cpf.isdigit() and len(cpf) == 11

def validar_nome():
    pass

# ================= AGENDAMENTOS =================

# Opção 2
def agendar_banho_tosa():
    print("\n🛁 AGENDAMENTO BANHO E TOSA")

    nome_cliente = input("Nome do cliente: ")
    #cliente = buscar_cliente(nome_cliente)

    cliente = banco_de_dados.pesquisar_usuario(banco, nome_cliente, "nome")

    if not cliente:
        print("❌ Cliente não cadastrado! Cadastre primeiro.\n")
        return

    nome_pet = input("Nome do pet: ")
    porte = input("Porte do pet (Pequeno/Médio/Grande): ")
    data = input("Data (dd/mm/aaaa): ")
    hora = input("Hora (hh:mm): ")

    data_hora = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")

    agendamento = {
        "tipo": "Banho e Tosa",
        "cliente": cliente,
        "pet": nome_pet,
        "porte": porte,
        "data_hora": data_hora
    }
    #   -----Mudar esse Trecho
    agendamentos_banho_tosa.append(agendamento)
    print("✅ Banho e tosa agendado com sucesso!\n")
    #   -----

# Opção 3
def agendar_clinico():
    print("\n🩺 AGENDAMENTO CLÍNICO")

    nome_cliente = input("Nome do cliente: ")
    cliente = buscar_cliente(nome_cliente)

    if not cliente:
        print("❌ Cliente não cadastrado! Cadastre primeiro.\n")
        return

    nome_pet = input("Nome do pet: ")
    especie = input("Espécie (Cão/Gato/etc): ")
    motivo = input("Motivo da consulta: ")
    data = input("Data (dd/mm/aaaa): ")
    hora = input("Hora (hh:mm): ")

    data_hora = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")

    agendamento = {
        "tipo": "Clínico",
        "cliente": cliente,
        "pet": nome_pet,
        "especie": especie,
        "motivo": motivo,
        "data_hora": data_hora
    }
    #   -----Mudar esse Trecho
    agendamentos_clinicos.append(agendamento)
    print("✅ Consulta clínica agendada com sucesso!\n")
    #   -----

def consultar_horarios():
    print("\n⏰ HORÁRIOS JÁ AGENDADOS\n")

    todos_agendamentos = agendamentos_banho_tosa + agendamentos_clinicos

    if not todos_agendamentos:
        print("Nenhum horário agendado. Todos estão disponíveis!\n")
        return

    for ag in sorted(todos_agendamentos, key=lambda x: x["data_hora"]):
        print(
            f"{ag['data_hora'].strftime('%d/%m/%Y %H:%M')} | "
            f"Tipo: {ag['tipo']} | "
            f"Cliente: {ag['cliente']['nome']} | "
            f"Pet: {ag['pet']}"
        )
    print()


# ================= RELATÓRIOS =================

# Opção 4
def relatorio_consultas():
    print("\n📊 RELATÓRIO DE CONSULTAS CLÍNICAS\n")

    #   -----Mudar esse Trecho
    if not agendamentos_clinicos:
        print("Nenhuma consulta clínica agendada.\n")
        return

    for ag in sorted(agendamentos_clinicos, key=lambda x: x["data_hora"]):
        print(
            f"{ag['data_hora'].strftime('%d/%m/%Y %H:%M')} | "
            f"Pet: {ag['pet']} | "
            f"Cliente: {ag['cliente']['nome']} | "
            f"Motivo: {ag['motivo']}"
        )
    print()
    #   -----

# Opção 7
def buscar_usuario(retorna_dados = False):
    x = banco_de_dados.pesquisar_usuario(banco.client, input("informe o cpf: "), True)

    if retorna_dados:
        return x
    else:
        for chave, valor in x:
            print(f"{chave} : {valor}")


    #print(banco_de_dados.pesquisar_usuario(link, input("cpf: ")) )

def buscar_cliente(nome):
    for cliente in clientes:
        if cliente["nome"].lower() == nome.lower():
            return cliente
    return None

# ================= MENU =================

def menu():
    while True:
        print("🐾 SISTEMA PETSHOP 🐾")
        print("1 - Cadastro de Cliente")
        print("2 - Agendamento Banho e Tosa")
        print("3 - Agendamento Clínico")
        print("4 - Relatório de Consultas Clínicas")
        print("5 - Consultar Horários Disponíveis")
        print("6 - Consultar Cliente Cadastrado")
        print("7 - Pesquisar Usuario (TESTES)")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            agendar_banho_tosa()
        elif opcao == "3":
            agendar_clinico()
        elif opcao == "4":
            relatorio_consultas()
        elif opcao == "5":
            consultar_horarios()
        elif opcao == "6":
            listar_clientes()
        elif opcao == "7":
            buscar_usuario()
        elif opcao == "0":
            print("👋 Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida!\n")

menu()
