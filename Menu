from datetime import datetime

clientes = []
agendamentos_banho_tosa = []
agendamentos_clinicos = []


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


def menu():
    while True:
        print("🐾 SISTEMA PETSHOP 🐾")
        print("1 - Cadastro de Cliente")
        print("2 - Agendamento Banho e Tosa")
        print("3 - Agendamento Clínico")
        print("4 - Relatório de Consultas")
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
        elif opcao == "0":
            print("👋 Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida!\n")

menu()
