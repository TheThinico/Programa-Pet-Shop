from datetime import datetime

clientes = []
agendamentos_banho_tosa = []
agendamentos_clinicos = []


# ================= CLIENTES =================

def cadastrar_cliente():
    print("\n👤 CADASTRO DE CLIENTE")

    nome = input("Nome do cliente: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")

    cliente = {
        "nome": nome,
        "telefone": telefone,
        "email": email
    }

    clientes.append(cliente)
    print("✅ Cliente cadastrado com sucesso!\n")


def buscar_cliente(nome):
    for cliente in clientes:
        if cliente["nome"].lower() == nome.lower():
            return cliente
    return None


def listar_clientes():
    print("\n📋 CLIENTES CADASTRADOS\n")

    if not clientes:
        print("Nenhum cliente cadastrado.\n")
        return

    for i, cliente in enumerate(clientes, start=1):
        print(
            f"{i} - Nome: {cliente['nome']} | "
            f"Telefone: {cliente['telefone']} | "
            f"E-mail: {cliente['email']}"
        )
    print()


# ================= AGENDAMENTOS =================

def agendar_banho_tosa():
    print("\n🛁 AGENDAMENTO BANHO E TOSA")

    nome_cliente = input("Nome do cliente: ")
    cliente = buscar_cliente(nome_cliente)

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

    agendamentos_banho_tosa.append(agendamento)
    print("✅ Banho e tosa agendado com sucesso!\n")


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

    agendamentos_clinicos.append(agendamento)
    print("✅ Consulta clínica agendada com sucesso!\n")


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

def relatorio_consultas():
    print("\n📊 RELATÓRIO DE CONSULTAS CLÍNICAS\n")

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


# ================= MENU =================

def menu():
    while True:
        print("🐾 SISTEMA PETSHOP 🐾")
        print("1 - Cadastro de Cliente")
        print("2 - Agendamento Banho e Tosa")
        print("3 - Agendamento Clínico")
        print("4 - Relatório de Consultas Clínicas")
        print("5 - Consultar Horários Disponíveis")
        print("6 - Consultar Clientes Cadastrados")
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
        elif opcao == "0":
            print("👋 Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida!\n")


menu()
