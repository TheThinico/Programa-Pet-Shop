from datetime import datetime

import banco_de_dados
import modelos
import requests

clientes = []
agendamentos_banho_tosa = []
agendamentos_clinicos = []

Banco = banco_de_dados.Db_Client()

# ================= CLIENTES =================

def cadastrar_usuario():
    print("\n👤 CADASTRO DE CLIENTE")

    nome = input("Nome do cliente: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    cpf = input("CPF: ") #validar_cpf(input("CPF: "))

    novo_cliente = modelos.Tutor(nome,telefone,email,cpf)
    banco_de_dados.salvar_tutor(Banco.link, novo_cliente.to_dict())

    #cadastrar_animal(novo_cliente)

    #clientes.append(cliente)
    #print("✅ Cliente cadastrado com sucesso!\n")

def cadastrar_pet():
    print("\n🐶 CADASTRO DE PET\n")

    # Primeiro, pede o CPF do tutor
    cpf_tutor = input("CPF do tutor: ")
    tutor = banco_de_dados.buscar_tutor_por_cpf(Banco.link, cpf_tutor)

    if not tutor:
        print("❌ Tutor não cadastrado! Cadastre o cliente primeiro.\n")
        return

    # Dados do pet
    nome_pet = input("Nome do pet: ")

    # Verifica se o pet já existe para o tutor
    pet_existente = banco_de_dados.buscar_animal_por_nome(Banco.link, nome_pet, cpf_tutor)
    if pet_existente:
        print(f"❌ Pet com o nome '{nome_pet}' já cadastrado para este tutor.\n")
        return

    tipo = input("Tipo de animal (Cão/Gato/Outro): ")
    raca = input("Raça: ")
    idade = input("Idade: ")

    novo_pet = modelos.Animal(nome_pet, tipo, raca, idade, cpf_tutor)
    banco_de_dados.salvar_animal(Banco.link, novo_pet.to_dict())

def buscar_endereco():
    cep = str(input("Digite o CEP: "))
    cep = cep.replace('-', '').replace(' ', '').replace('.', '').replace(',', '')
    if len(cep) == 8:
        link = f"https://viacep.com.br/ws/{cep}/json/"
        requisicao = requests.get(link)

        dic_requisicao = requisicao.json()
        uf = dic_requisicao["uf"]
        cidade = dic_requisicao['localidade']
        bairro = dic_requisicao['bairro']
        logradouro = dic_requisicao['logradouro']

        print(f'Voce mora no {uf}, na cidade {cidade}, o bairro {bairro} e o logradouro {logradouro}')
    else:
        print('CEP INVÁLIDO')

# ================= AGENDAMENTOS =================

def agendar_banho_e_tosa():
    print("\n🛁 AGENDAMENTO BANHO E TOSA")

    cpf_tutor = input("CPF do tutor: ")
    tutor = banco_de_dados.buscar_tutor_por_cpf(Banco.link, cpf_tutor)
    if not tutor:
        print("❌ Cliente não encontrado!")
        return

    nome_pet = input("Nome do pet: ")
    tutor_animal = banco_de_dados.buscar_animal_por_nome(Banco.link, nome_pet, tutor["cpf"])
    if not tutor_animal:
        print("❌ Pet não encontrado para este cliente! Cadastre o pet primeiro.")
        return

    porte = input("Porte do pet (Pequeno/Médio/Grande): ")
    data = input("Data (dd/mm/aaaa): ")
    hora = input("Hora (hh:mm): ")

    try:
        data_hora = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")
    except ValueError:
        print("❌ Formato de data/hora inválido!")
        return

    agendamento = {
        "porte": porte,
        "data_hora": data_hora,
        "tutor_cpf": tutor["cpf"],
        "cliente_nome": tutor["nome"],
        "animal_nome": tutor_animal["nome"]
    }

    colecao = Banco.link["banco"]["agendamento_banho_tosa"]
    try:
        colecao.insert_one(agendamento)
        print("✅ Agendamento de banho e tosa cadastrado com sucesso!")
    except Exception as e:
        print("❌ Erro ao salvar o agendamento:", e)

def agendar_clinico_pet():
    print("\n🩺 AGENDAMENTO CLÍNICO DO PET")

    cpf_tutor = input("CPF do tutor: ")
    tutor = banco_de_dados.buscar_tutor_por_cpf(Banco.link, cpf_tutor)
    if not tutor:
        print("❌ Cliente não encontrado!")
        return

    nome_pet = input("Nome do pet: ")
    tutor_animal = banco_de_dados.buscar_animal_por_nome(Banco.link, nome_pet, tutor["cpf"])
    if not tutor_animal:
        print("❌ Pet não encontrado para este cliente! Cadastre o pet primeiro.")
        return

    porte = input("Porte do pet (Pequeno/Médio/Grande): ")
    data = input("Data (dd/mm/aaaa): ")
    hora = input("Hora (hh:mm): ")

    try:
        data_hora = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")
    except ValueError:
        print("❌ Formato de data/hora inválido!")
        return

    agendamento = {
        "data_hora": data_hora,
        "tutor_cpf": tutor["cpf"],
        "cliente_nome": tutor["nome"],
        "animal_nome": tutor_animal["nome"],
        "porte": porte
    }

    banco_de_dados.salvar_agendamento_clinico(Banco.link, agendamento, {"nome": nome_pet})
    print("✅ Consulta clínica agendada com sucesso!\n")

# ================= RELATÓRIOS =================

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

def listar_clientes():
    print("\n📋 CLIENTES CADASTRADOS\n")

    clientes = banco_de_dados.listar_clientes(Banco.link)

    if not clientes:
        print("Nenhum cliente cadastrado.\n")
        return

    for i, f in enumerate(clientes, start=1):
        print(f"\n{i}️⃣ CLIENTE")
        for k, v in f.items():
            print(f"{k}: {v}")

def buscar_cliente():
    print("\n🔍 BUSCAR CLIENTE")
    cpf = input("CPF: ")

    clientes = banco_de_dados.buscar_clientes_banco(Banco.link, cpf)

    if not clientes:
        print("❌ Cliente não encontrado.\n")
        return

    print("\n👤 DADOS DO CLIENTE")
    for k, v in clientes.items():
        print(f"{k}: {v}")

def atualizar_cliente():
    print("\n✏️ ATUALIZAR CLIENTE")
    cpf = input("CPF do cliente: ")

    tutor = banco_de_dados.buscar_cliente(Banco.link, cpf)

    if not clientes:
        print("❌ Cliente não encontrado.\n")
        return

    print("Pressione ENTER para manter o valor atual\n")

    novos_dados = {
        "cpf": input(f"CPF ({tutor['cpf']}): ") or tutor["cpf"],
        "nome": input(f"Nome ({tutor['nome']}): ") or tutor["nome"],
        "idade": input(f"Idade ({tutor['idade']}): ") or tutor["idade"],
        "sexo": input(f"Sexo ({tutor['sexo']}): ") or tutor["sexo"],
        "endereco": input(f"Endereço ({tutor['endereco']}): ") or tutor["endereco"],
        "telefone": input(f"Telefone ({tutor['telefone']}): ") or tutor["telefone"],
        "email": input(f"E-mail ({tutor['email']}): ") or tutor["email"],
    }

def excluir_cliente():
    print("\n🗑 EXCLUIR CLIENTE")
    cpf = input("CPF do funcionário: ")

    tutor = banco_de_dados.buscar_clientes_banco(Banco.link, cpf)

    if not clientes:
        print("❌ Cliente não encontrado.\n")
        return

    confirm = input(f"Tem certeza que deseja excluir {tutor['nome']}? (S/N): ")

    if confirm.lower() == "s":
        banco_de_dados.excluir_clientes_banco(Banco.link, cpf)
        print("✅ Cliente excluído com sucesso!\n")
    else:
        print("❌ Operação cancelada.\n")

# ====================== FUNCIONÁRIOS =======================

#✅ CREATE
def cadastrar_funcionario():
    print("\n👤 CADASTRO DE FUNCIONARIOS")

    cpf = input("CPF (id): ")
    nome = input("Nome do Funcionário: ")
    idade = input("Idade: ")
    sexo = input("Sexo: ")
    endereco = input("Endereço: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    funcao = input("Função: ")

    funcionario = {

        "cpf": cpf,
        "nome": nome,
        "idade": idade,
        "sexo": sexo,
        "endereco": endereco,
        "telefone": telefone,
        "email": email,
        "funcao": funcao

    }

    banco_de_dados.salvar_funcionario_banco(Banco.link, funcionario)
    print("✅ Funcionário cadastrado com sucesso no MongoDB!\n")

#🔍 READ – Buscar funcionário
def listar_funcionarios():
    print("\n📋 FUNCIONÁRIOS CADASTRADOS\n")

    funcionarios = banco_de_dados.listar_funcionarios_banco(Banco.link)

    if not funcionarios:
        print("Nenhum funcionário cadastrado.\n")
        return

    for i, f in enumerate(funcionarios, start=1):
        print(f"\n{i}️⃣ FUNCIONÁRIO")
        for k, v in f.items():
            print(f"{k}: {v}")

def buscar_funcionario():
    print("\n🔍 BUSCAR FUNCIONÁRIO")
    cpf = input("CPF do funcionário: ")

    funcionario = banco_de_dados.buscar_funcionario_banco(Banco.link, cpf)

    if not funcionario:
        print("❌ Funcionário não encontrado.\n")
        return

    print("\n👤 DADOS DO FUNCIONÁRIO")
    for k, v in funcionario.items():
        print(f"{k}: {v}")

def atualizar_funcionario():
    print("\n✏️ ATUALIZAR FUNCIONÁRIO")
    cpf = input("CPF do funcionário: ")

    funcionario = banco_de_dados.buscar_funcionario_banco(Banco.link, cpf)

    if not funcionario:
        print("❌ Funcionário não encontrado.\n")
        return

    print("Pressione ENTER para manter o valor atual\n")

    novos_dados = {
        "nome": input(f"Nome ({funcionario['nome']}): ") or funcionario["nome"],
        "idade": input(f"Idade ({funcionario['idade']}): ") or funcionario["idade"],
        "sexo": input(f"Sexo ({funcionario['sexo']}): ") or funcionario["sexo"],
        "endereco": input(f"Endereço ({funcionario['endereco']}): ") or funcionario["endereco"],
        "telefone": input(f"Telefone ({funcionario['telefone']}): ") or funcionario["telefone"],
        "email": input(f"E-mail ({funcionario['email']}): ") or funcionario["email"],
        "funcao": input(f"Função ({funcionario['funcao']}): ") or funcionario["funcao"],
    }

    banco_de_dados.atualizar_funcionario_banco(Banco.link, cpf, novos_dados)
    print("✅ Funcionário atualizado com sucesso!\n")

def excluir_funcionario():
    print("\n🗑 EXCLUIR FUNCIONÁRIO")
    cpf = input("CPF do funcionário: ")

    funcionario = banco_de_dados.buscar_funcionario_banco(Banco.link, cpf)

    if not funcionario:
        print("❌ Funcionário não encontrado.\n")
        return

    confirm = input(f"Tem certeza que deseja excluir {funcionario['nome']}? (S/N): ")

    if confirm.lower() == "s":
        banco_de_dados.excluir_funcionario_banco(Banco.link, cpf)
        print("✅ Funcionário excluído com sucesso!\n")
    else:
        print("❌ Operação cancelada.\n")

def buscar_usuario(retorna = False):
    x = banco_de_dados.buscar_tutor_por_cpf(Banco.link, input("informe o cpf: "), True)

    if retorna:
        return x
    else:
        for chave, valor in x:
            print(f"{chave} : {valor}")

    #print(banco_de_dados.pesquisar_usuario(link, input("cpf: ")) )


# ================= MENU =================

def menu():
    while True:
        print("")
        print("----------------------------------")
        print("     🐾 SISTEMA PETSHOP 🐾")
        print("----------------------------------")
        print("1 - Cadastro de Cliente")
        print("2 - Cadastro de Pets")
        print("3 - Agendamento Clínico do Pet")
        print("4 - Agendamento Banho e Tosa")
        print("-----------------------------------")
        print("5 - Relatório de Consultas Clínicas")
        print("6 - Consultar Horários Disponíveis")
        print("7 - Consultar Clientes Cadastrados")
        print("8 - Consultar Funcionarios Cadastrados")
        print("--------------------------------------")
        print("9  - Cadastro de Funcionários")
        print("10 - Buscar Funcionário")
        print("11 - Atualizar Funcionário")
        print("12 - Excluir Funcionário")
        print("")
        print("0 - Sair <====")
        print("")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            cadastrar_pet()
        elif opcao == "3":
            agendar_clinico_pet()
        elif opcao == "4":
            agendar_banho_e_tosa()
        elif opcao == "5":
            relatorio_consultas()
        elif opcao == "6":
            consultar_horarios()
        elif opcao == "7":
            listar_clientes()
        elif opcao == "8":
            listar_funcionarios()
        elif opcao == "9":
            cadastrar_funcionario()
        elif opcao == "10":
            buscar_funcionario()
        elif opcao == "11":
            atualizar_funcionario()
        elif opcao == "12":
            excluir_funcionario()
        elif opcao == "0":
            print("👋 Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida!\n")
menu()