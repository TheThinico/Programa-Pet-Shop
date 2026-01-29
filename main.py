from datetime import datetime, timedelta

import banco_de_dados
import modelos
import requests

clientes = []
agendamentos_banho_tosa = []
agendamentos_clinicos = []

Banco = banco_de_dados.Db_Client()

# ================= CLIENTE/ANIMAL =================
def cadastrar_usuario():
    print("\n👤 CADASTRO DE CLIENTE")

    cpf = input("CPF: ") # validar_cpf(input("CPF: "))
    nome = input("Nome do cliente: ")
    idade = input("Idade: ")
    sexo = input("Sexo (1 = masculino, 2 = feminino): ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    endereco = buscar_endereco()

    novo_tutor = modelos.Tutor()
    novo_tutor.set_dados(cpf,nome,idade,sexo,telefone,email,endereco)

    banco_de_dados.salvar_tutor(Banco.database, novo_tutor)

    # novo_cliente.inserir_dados(cpf, nome, idade, sexo, telefone, email, endereco)
    # print(novo_cliente)
    # print(novo_cliente.to_dict())

def cadastrar_pet():
    print("\n🐶 CADASTRO DE PET\n")

    # Primeiro, pede o CPF do tutor
    cpf_tutor = input("CPF do tutor: ")
    tutor = banco_de_dados.buscar_tutor_por_cpf(Banco.database, cpf_tutor)
    if tutor == None:
        print("❌ Tutor não cadastrado! Cadastre o cliente primeiro.\n")
        return

    # Dados do pet
    nome_animal = input("Nome do pet: ")

    # Verifica se o pet já existe para o tutor
    animal = banco_de_dados.buscar_animal_por_nome(Banco.database, nome_animal, cpf_tutor)
    if animal:
        print(f"❌ Pet com o nome '{nome_animal}' já cadastrado para este tutor.\n")
        return

    tipo = input("Tipo de animal (Cão/Gato/Outro): ")
    raca = input("Raça: ")
    idade = input("Idade: ")

    novo_pet = modelos.Animal()
    novo_pet.set_dados(nome_animal, tipo, raca, idade, tutor.cpf)
    banco_de_dados.salvar_animal(Banco.database, novo_pet)

# ================= SERVIÇOS =================
def agendar_servico():
    print("\n AGENDAMENTO ")

    cpf_tutor = input("CPF do tutor: ")
    tutor_buscar = banco_de_dados.buscar_tutor_por_cpf(Banco.database, cpf_tutor)
    if not tutor_buscar:
        print("❌ Cliente não encontrado!")
        return

    tutor = modelos.Tutor()
    tutor.set_dict(tutor_buscar)

    # nome_pet = input("Nome do pet: ")
    # tutor_animal = banco_de_dados.buscar_animal_por_nome(Banco.database, nome_pet, tutor["cpf"])
    # if not tutor_animal:
    #     print("❌ Pet não encontrado para este cliente! Cadastre o pet primeiro.")
    #     return

    animal_buscar = escolher_animais_do_tutor(tutor)
    tutor_animal= modelos.Animal()
    tutor_animal.set_dict(animal_buscar)

    tipo_servico = escolher_tipo_servico()

    #porte = input("Porte do pet (Pequeno/Médio/Grande): ")
    data = input("Data (dd/mm/aaaa): ").strip()
    hora = input("Hora (hh:mm): ").strip()

    try:
        data_hora = datetime.strptime(
            f"{data} {hora}",
            "%d/%m/%Y %H:%M"
        )
    except ValueError:
        print("❌ Formato de data/hora inválido!")
        return

    agendamento = {
        "cliente_nome": tutor.nome,
        "tutor_cpf": tutor.cpf,
        "animal_nome": tutor_animal.nome,
        #"porte": porte
        "tipo": tipo_servico,
        "data": data,
        "hora": hora,
    }

    banco_de_dados.salvar_agendamento_servico(Banco.database, agendamento)

    if tipo_servico == 1:
        print("✅ Banho e Tosa agendado com sucesso!\n")
    elif tipo_servico == 2:
        print("✅ Consulta clínica agendada com sucesso!\n")

# ====================== FUNCIONÁRIOS =======================
def cadastrar_funcionario():
    print("\n👤 CADASTRO DE FUNCIONARIOS")

    cpf = input("CPF: ")
    nome = input("Nome do Funcionário: ")
    idade = input("Idade: ")
    sexo = input("Sexo: ")

    telefone = input("Telefone: ")
    email = input("E-mail: ")

    endereco = buscar_endereco()

    funcao = input("Função: ")
    status = int(input("Status (1- ativo| 2- afastado| 0- desligado): "))

    novo_funcionario = modelos.Funcionario()
    novo_funcionario.set_dados(cpf,nome,idade,sexo, telefone, email, endereco, funcao, status)

    banco_de_dados.salvar_funcionario(Banco.database, novo_funcionario)

def listar_funcionarios():
    print("\n📋 FUNCIONÁRIOS CADASTRADOS\n")

    funcionarios = banco_de_dados.lista_funcionarios(Banco.database)

    if not funcionarios:
        print("Nenhum funcionário cadastrado.\n")
        return

    for i in range(len(funcionarios)):
        print (f"{i})")
        for j in funcionarios:
            print(f"  {funcionarios[i]["nome"]}")
            print(f"  {funcionarios[i]["idade"]}")
            print(f"  {funcionarios[i]["funcao"]}")
            if funcionarios[i]["status"] == 1:
                print(f"  ativo")
            elif funcionarios[i]["status"] == 2:
                print(f"  afastado")
            elif funcionarios[i]["status"] == 0:
                print(f"  desligado")
            else:
                print(f"  NA")

    # for i, f in enumerate(funcionarios, funcionarios[i]):
    #     print(f"\n{i}️⃣ FUNCIONÁRIO")
    #     for k, v in f.items():
    #         print(f"{k}: {v}")

def buscar_funcionario():
    print("\n🔍 BUSCAR FUNCIONÁRIO")

    cpf = input("CPF do funcionário: ")
    funcionario = banco_de_dados.buscar_funcionario(Banco.database, cpf)

    if funcionario == None:
        print("❌ Funcionário não encontrado.\n")
        return

    print("\n👤 DADOS DO FUNCIONÁRIO")
    for k, v in funcionario.to_dict().items():
        print(f"{k}: {v}")

# ================= RELATÓRIOS =================
def pesquisar_cliente():
    cpf_tutor = input("CPF do tutor: ")
    tutor = banco_de_dados.buscar_tutor_por_cpf(Banco.database, cpf_tutor)
    if tutor == None:
        print("❌ Tutor não cadastrado! Cadastre o cliente primeiro.\n")
        return

    animais = banco_de_dados.buscar_animais_tutor(Banco.database, cpf_tutor)

    for i, j in tutor.to_dict().items():
        print(f"{i}: {j}")
    #tutor_dic = tutor.to_dict()
    # for i in tutor_dic:
    #     print(f"{i}: {tutor_dic[i]}")

    if animais[0] == None:
        print(f"\n--- Tutor não Possui animais Cadastrados ---")
    else:
        for i in range(len(animais)):
            print(f"{i}) ")
            for j, k in animais[i].to_dict().items():
                print(f"{j}: {k}")

def consultar_horarios():
    print("\n⏰ HORÁRIOS JÁ AGENDADOS\n")
    pass

# ================= FUNÇÕES AUXILIARES =================
def buscar_endereco():
    cep = str(input("Digite o CEP: "))
    cep = cep.replace('-', '').replace(' ', '').replace('.', '').replace(',', '')
    if len(cep) == 8:
        link = f"https://viacep.com.br/ws/{cep}/json/"
        requisicao = requests.get(link)

        dic_requisicao = requisicao.json()
        print(f"{dic_requisicao["logradouro"]}, Bairro {dic_requisicao['bairro']}, {dic_requisicao['localidade']}")
        numero = input("Numero: ")
        complemento = input("Complemento (se não possuir: N): ")

        endereco = {
            "cep": cep,
            "rua": dic_requisicao['logradouro'],
            "numero": numero,
            "complemento": complemento,
            "bairro": dic_requisicao['bairro'],
            "cidade": dic_requisicao['localidade'],
            "uf": dic_requisicao["uf"],
        }

        return endereco
    else:
        raise Exception("CEP INVÁLIDO")

def escolher_animais_do_tutor(tutor):
    animais = banco_de_dados.buscar_animais_tutor(Banco.database, tutor.cpf)

    if animais == None:
        raise ValueError("Erro: não achamos animais cadastrados")
    elif len(animais) == 1:
        return animais[0]
    else:
        while True:
            count = 0
            for list in animais:
                count += 1
                print(f"{count}) {list["nome"]}")
            escolha = int(input("Qual animal: "))
            if escolha >= 1 and escolha <= count:
                return animais[count - 1]
            else:
                print("Opção não existente")

def escolher_tipo_servico():
    while True:
        servico = int(input("1 - Banho e Tosa \n2 - Clinico\n"))
        if servico == 1 or servico == 2:
            return servico
        else:
            print("Opção inválida.")

def gerar_horarios_time(inicio="08:00", fim="18:00", intervalo=30):
    horarios = []

    atual = datetime.strptime(inicio, "%H:%M")
    fim = datetime.strptime(fim, "%H:%M")

    while atual <= fim:
        #print(atual.time())
        horarios.append(atual.time())
        atual += timedelta(minutes=intervalo)

    return horarios

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
        print("4 - Pesquisar Cliente ")
        print("-----------------------------------")
        print("5 - Relatório de Consultas Clínicas")
        print("6 - Consultar Horários Disponíveis")
        print("7")
        #print("7 - Consultar Clientes Cadastrados")
        print("8 - Consultar Funcionarios Cadastrados")
        print("--------------------------------------")
        print("9  - Cadastro de Funcionários")
        print("10 - Buscar Funcionário")
        print("11")
        # print("11 - Atualizar Funcionário")
        # print("12 - Excluir Funcionário")
        print("")
        print("0 - Sair <====")
        print("")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            cadastrar_pet()
        elif opcao == "3":
            agendar_servico()
        elif opcao == "4":
             pesquisar_cliente()
        #elif opcao == "5":
            #relatorio_servicos()
        elif opcao == "6":
            consultar_horarios()
        # elif opcao == "7":
        #     listar_clientes()
        elif opcao == "8":
            listar_funcionarios()
        elif opcao == "9":
            cadastrar_funcionario()
        elif opcao == "10":
            buscar_funcionario()
        # elif opcao == "11":
        #     atualizar_funcionario()
        # elif opcao == "12":
        #     excluir_funcionario()
        elif opcao == "0":
            print("👋 Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida!\n")
menu()

# def buscar_cliente():
#     print("\n🔍 BUSCAR CLIENTE")
#     cpf = input("CPF: ")
#
#     clientes = banco_de_dados.buscar_clientes(Banco.database, cpf)
#
#     if not clientes:
#         print("❌ Cliente não encontrado.\n")
#         return
#
#     print("\n👤 DADOS DO CLIENTE")
#     for k, v in clientes.items():
#         print(f"{k}: {v}")

# def excluir_funcionario():
#     print("\n🗑 EXCLUIR FUNCIONÁRIO")
#     cpf = input("CPF do funcionário: ")
#
#     funcionario = banco_de_dados.buscar_funcionario(Banco.database, cpf)
#
#     if not funcionario:
#         print("❌ Funcionário não encontrado.\n")
#         return
#
#     confirm = input(f"Tem certeza que deseja excluir {funcionario['nome']}? (S/N): ")
#
#     if confirm.lower() == "s":
#         banco_de_dados.excluir_funcionario_banco(Banco.database, cpf)
#         print("✅ Funcionário excluído com sucesso!\n")
#     else:
#         print("❌ Operação cancelada.\n")

# def atualizar_funcionario():
#     print("\n✏️ ATUALIZAR FUNCIONÁRIO")
#     cpf = input("CPF do funcionário: ")
#
#     funcionario = banco_de_dados.buscar_funcionario_banco(Banco.database, cpf)
#
#     if not funcionario:
#         print("❌ Funcionário não encontrado.\n")
#         return
#
#     print("Pressione ENTER para manter o valor atual\n")
#
#     novos_dados = {
#         "nome": input(f"Nome ({funcionario['nome']}): ") or funcionario["nome"],
#         "idade": input(f"Idade ({funcionario['idade']}): ") or funcionario["idade"],
#         "sexo": input(f"Sexo ({funcionario['sexo']}): ") or funcionario["sexo"],
#         "endereco": input(f"Endereço ({funcionario['endereco']}): ") or funcionario["endereco"],
#         "telefone": input(f"Telefone ({funcionario['telefone']}): ") or funcionario["telefone"],
#         "email": input(f"E-mail ({funcionario['email']}): ") or funcionario["email"],
#         "funcao": input(f"Função ({funcionario['funcao']}): ") or funcionario["funcao"],
#     }
#
#     banco_de_dados.atualizar_funcionario_banco(Banco.database, cpf, novos_dados)
#     print("✅ Funcionário atualizado com sucesso!\n")


# def atualizar_cliente():
#     print("\n✏️ ATUALIZAR CLIENTE")
#     cpf = input("CPF do cliente: ")
#
#     tutor = banco_de_dados.buscar_cliente(Banco.link, cpf)
#
#     if not clientes:
#         print("❌ Cliente não encontrado.\n")
#         return
#
#     print("Pressione ENTER para manter o valor atual\n")
#
#     novos_dados = {
#         "cpf": input(f"CPF ({tutor['cpf']}): ") or tutor["cpf"],
#         "nome": input(f"Nome ({tutor['nome']}): ") or tutor["nome"],
#         "idade": input(f"Idade ({tutor['idade']}): ") or tutor["idade"],
#         "sexo": input(f"Sexo ({tutor['sexo']}): ") or tutor["sexo"],
#         "endereco": input(f"Endereço ({tutor['endereco']}): ") or tutor["endereco"],
#         "telefone": input(f"Telefone ({tutor['telefone']}): ") or tutor["telefone"],
#         "email": input(f"E-mail ({tutor['email']}): ") or tutor["email"],
#     }

# def excluir_cliente():
#     print("\n🗑 EXCLUIR CLIENTE")
#     cpf = input("CPF do funcionário: ")
#
#     tutor = banco_de_dados.buscar_tutor_por_cpf(Banco.database, cpf)
#
#     if not clientes:
#         print("❌ Cliente não encontrado.\n")
#         return
#
#     confirm = input(f"Tem certeza que deseja excluir {tutor['nome']}? (S/N): ")
#
#     if confirm.lower() == "s":
#         banco_de_dados.excluir_clientes_banco(Banco.database, cpf)
#         print("✅ Cliente excluído com sucesso!\n")
#     else:
#         print("❌ Operação cancelada.\n")

# def buscar_usuario(retorna = False):
#     x = banco_de_dados.buscar_tutor_por_cpf(Banco.database, input("informe o cpf: "), True)
#
#     if retorna:
#         return x
#     else:
#         for chave, valor in x:
#             print(f"{chave} : {valor}")
#     #print(banco_de_dados.pesquisar_usuario(link, input("cpf: ")) )

# def agendar_banho_e_tosa():
#     print("\n🛁 AGENDAMENTO BANHO E TOSA")
#
#     cpf_tutor = input("CPF do tutor: ")
#     tutor = banco_de_dados.buscar_tutor_por_cpf(Banco.database, cpf_tutor)
#     if not tutor:
#         print("❌ Cliente não encontrado!")
#         return
#
#     nome_pet = input("Nome do pet: ")
#     tutor_animal = banco_de_dados.buscar_animal_por_nome(Banco.database, nome_pet, tutor["cpf"])
#     if not tutor_animal:
#         print("❌ Pet não encontrado para este cliente! Cadastre o pet primeiro.")
#         return
#
#     porte = input("Porte do pet (Pequeno/Médio/Grande): ")
#     data = input("Data (dd/mm/aaaa): ")
#     hora = input("Hora (hh:mm): ")
#
#     try:
#         data_hora = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")
#     except ValueError:
#         print("❌ Formato de data/hora inválido!")
#         return
#
#     agendamento = {
#         "data_hora": data_hora,
#         "tutor_cpf": tutor["cpf"],
#         "cliente_nome": tutor["nome"],
#         "animal_nome": tutor_animal["nome"],
#         "porte": porte
#     }
#
#     banco_de_dados.salvar_agendamento_banho_tosa(Banco.database, agendamento)
#     print("✅ Banho e Tosa agendado com sucesso!\n")
#
# def agendar_clinico_pet():
#     print("\n🩺 AGENDAMENTO CLÍNICO DO PET")
#
#     cpf_tutor = input("CPF do tutor: ")
#     tutor = banco_de_dados.buscar_tutor_por_cpf(Banco.database, cpf_tutor)
#     if not tutor:
#         print("❌ Cliente não encontrado!")
#         return
#
#     nome_pet = input("Nome do pet: ")
#     tutor_animal = banco_de_dados.buscar_animal_por_nome(Banco.database, nome_pet, tutor["cpf"])
#     if not tutor_animal:
#         print("❌ Pet não encontrado para este cliente! Cadastre o pet primeiro.")
#         return
#
#     porte = input("Porte do pet (Pequeno/Médio/Grande): ")
#     data = input("Data (dd/mm/aaaa): ")
#     hora = input("Hora (hh:mm): ")
#
#     try:
#         data_hora = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")
#     except ValueError:
#         print("❌ Formato de data/hora inválido!")
#         return
#
#     agendamento = {
#         "data_hora": data_hora,
#         "tutor_cpf": tutor["cpf"],
#         "cliente_nome": tutor["nome"],
#         "animal_nome": tutor_animal["nome"],
#         "porte": porte
#     }
#
#     banco_de_dados.salvar_agendamento_clinico(Banco.database,agendamento)
#     print("✅ Consulta clínica agendada com sucesso!\n")

# def listar_clientes():
#     print("\n📋 CLIENTES CADASTRADOS\n")
#
#     clientes = banco_de_dados.listar_clientes(Banco.database)
#
#     if not clientes:
#         print("Nenhum cliente cadastrado.\n")
#         return
#
#     for i, f in enumerate(clientes, start=1):
#         print(f"\n{i}️⃣ CLIENTE")
#         for k, v in f.items():
#             print(f"{k}: {v}")
